from flask import Blueprint, request, jsonify, Response
from database import db
from models import StudySpot
from datetime import datetime
from collections import OrderedDict
import logging
import re
import threading
import time
from urllib.parse import parse_qs, urlparse
from urllib import request as urllib_request, error as urllib_error
from url_utils import normalize_picture_urls

# Configure logging
logger = logging.getLogger(__name__)

# Create Blueprint
api_bp = Blueprint('api', __name__)


# Middleware for logging requests
@api_bp.before_request
def log_request():
    """Log all incoming requests."""
    logger.info(f"{request.method} {request.path}")


# Error handlers
@api_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Resource not found'}), 404


@api_bp.errorhandler(400)
def bad_request(error):
    """Handle 400 errors."""
    return jsonify({'error': 'Bad request'}), 400


@api_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


# Health check endpoint
@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Longhorn Studies API is running',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


# Required fields for create
STUDY_SPOT_REQUIRED = {
    'abbreviation', 'study_spot_name', 'address', 'noise_level',
    'capacity', 'spot_type', 'access_hours', 'near_food', 'reservable', 'description', 'pictures', 'tags'
}

TIME_PATTERN = re.compile(r'^([01]\d|2[0-3]):([0-5]\d)$')
DRIVE_FILE_PATH_RE = re.compile(r'/file/d/([A-Za-z0-9_-]+)')
SPOT_IMAGE_PATH_RE = re.compile(r'/api/study_spots/(\d+)/images/(\d+)/?$')
LOCAL_HOSTNAMES = {'localhost', '127.0.0.1', '::1'}
IMAGE_CACHE_MAX_ENTRIES = 256
IMAGE_CACHE_TTL_SECONDS = 3600
IMAGE_CACHE = OrderedDict()
IMAGE_CACHE_LOCK = threading.Lock()


def _normalize_access_hours(value):
    """
    Validate and normalize access_hours into a 7-day list:
    [["HH:MM", "HH:MM"], ...] where index 0=Monday ... 6=Sunday.
    """
    if not isinstance(value, list) or len(value) != 7:
        raise ValueError("access_hours must be an array with 7 elements")

    normalized = []
    for day in value:
        if not isinstance(day, list) or len(day) != 2:
            raise ValueError("Each access_hours day must be a 2-item array: [open, close]")
        open_time, close_time = day
        if not isinstance(open_time, str) or not isinstance(close_time, str):
            raise ValueError("Open/close times must be strings in HH:MM format")
        if not TIME_PATTERN.match(open_time) or not TIME_PATTERN.match(close_time):
            raise ValueError("Open/close times must be in HH:MM (24-hour) format")
        normalized.append([open_time, close_time])
    return normalized


def _extract_google_drive_file_id(url):
    """Extract Google Drive file id from common URL formats."""
    parsed = urlparse(url)
    hostname = (parsed.hostname or '').lower()

    if 'drive.google.com' not in hostname and 'docs.google.com' not in hostname:
        return None

    path_match = DRIVE_FILE_PATH_RE.search(parsed.path or '')
    if path_match:
        return path_match.group(1)

    query_params = parse_qs(parsed.query or '')
    file_id = query_params.get('id', [None])[0]
    if file_id:
        return file_id

    return None


def _is_safe_remote_url(url):
    """Basic SSRF protection for proxy endpoint."""
    parsed = urlparse(url)
    if parsed.scheme not in {'http', 'https'}:
        return False
    hostname = (parsed.hostname or '').lower()
    if not hostname:
        return False
    if hostname in LOCAL_HOSTNAMES:
        return False
    return True


def _candidate_proxy_urls(url):
    """
    Build candidate image URLs.
    For Google Drive, try several direct variants since availability differs per file.
    """
    file_id = _extract_google_drive_file_id(url)
    if not file_id:
        return [url]

    # Prefer direct image variants first to avoid slow HTML responses.
    candidates = [
        f'https://drive.google.com/thumbnail?id={file_id}&sz=w1200',
        f'https://lh3.googleusercontent.com/d/{file_id}=w1200',
        f'https://drive.google.com/uc?export=download&id={file_id}',
        f'https://docs.google.com/uc?export=download&id={file_id}',
        f'https://drive.google.com/uc?export=view&id={file_id}',
        url,
    ]
    return list(dict.fromkeys(candidates))


def _fetch_remote_image(url):
    req = urllib_request.Request(
        url,
        headers={
            'User-Agent': 'LonghornStudiesImageProxy/1.0',
            'Accept': 'image/*,*/*;q=0.8',
        }
    )

    with urllib_request.urlopen(req, timeout=15) as upstream:
        content_type = (upstream.headers.get('Content-Type') or '').split(';', 1)[0].strip().lower()
        body = upstream.read()
        return body, content_type


def _build_image_response(body, content_type):
    response = Response(body, status=200, content_type=content_type)
    response.headers['Cache-Control'] = f'public, max-age={IMAGE_CACHE_TTL_SECONDS}'
    return response


def _get_cached_image(url):
    now = time.time()
    with IMAGE_CACHE_LOCK:
        cached = IMAGE_CACHE.get(url)
        if cached is None:
            return None

        expires_at = cached['expires_at']
        if expires_at <= now:
            del IMAGE_CACHE[url]
            return None

        IMAGE_CACHE.move_to_end(url)
        return cached['body'], cached['content_type']


def _set_cached_image(url, body, content_type):
    with IMAGE_CACHE_LOCK:
        IMAGE_CACHE[url] = {
            'body': body,
            'content_type': content_type,
            'expires_at': time.time() + IMAGE_CACHE_TTL_SECONDS,
        }
        IMAGE_CACHE.move_to_end(url)

        while len(IMAGE_CACHE) > IMAGE_CACHE_MAX_ENTRIES:
            IMAGE_CACHE.popitem(last=False)


def _proxy_image_from_remote_url(raw_url):
    """Fetch and proxy an image from a remote URL."""
    errors = []
    if not _is_safe_remote_url(raw_url):
        return None, ['Unsupported or unsafe URL']

    for candidate in _candidate_proxy_urls(raw_url):
        if not _is_safe_remote_url(candidate):
            errors.append(f'unsupported candidate URL: {candidate}')
            continue

        cached = _get_cached_image(candidate)
        if cached is not None:
            body, content_type = cached
            return _build_image_response(body, content_type), errors

        try:
            body, content_type = _fetch_remote_image(candidate)
            if not content_type.startswith('image/'):
                errors.append(f'non-image content-type from {candidate}: {content_type or "unknown"}')
                continue

            _set_cached_image(candidate, body, content_type)
            return _build_image_response(body, content_type), errors
        except urllib_error.HTTPError as err:
            errors.append(f'HTTP {err.code} from {candidate}')
        except urllib_error.URLError as err:
            errors.append(f'URL error from {candidate}: {err.reason}')
        except Exception as err:
            errors.append(f'Unexpected error from {candidate}: {err}')

    return None, errors


def _spot_image_endpoint_url(spot_id, image_index):
    """Build a stable image endpoint URL for a specific spot image index."""
    base = request.url_root.rstrip('/')
    return f'{base}/api/study_spots/{spot_id}/images/{image_index}'


def _get_spot_picture_url_by_index(spot, image_index):
    """Return the normalized remote picture URL at index, or None if invalid."""
    pictures = normalize_picture_urls(spot.pictures)
    if image_index < 0 or image_index >= len(pictures):
        return None
    picture_url = pictures[image_index]
    if not isinstance(picture_url, str):
        return None
    picture_url = picture_url.strip()
    if not picture_url:
        return None
    return picture_url


def _resolve_spot_image_endpoint_url(url, current_spot=None):
    """Resolve /api/study_spots/<id>/images/<index> URLs to original remote URLs."""
    parsed = urlparse(url)
    path = parsed.path or ''
    match = SPOT_IMAGE_PATH_RE.match(path)
    if not match:
        return url

    source_spot_id = int(match.group(1))
    source_image_index = int(match.group(2))

    if current_spot is not None and current_spot.id == source_spot_id:
        source_spot = current_spot
    else:
        source_spot = StudySpot.query.get(source_spot_id)

    if source_spot is None:
        return url

    resolved = _get_spot_picture_url_by_index(source_spot, source_image_index)
    return resolved if resolved is not None else url


def _normalize_incoming_pictures(pictures, current_spot=None):
    """Normalize incoming pictures and unwrap internal image endpoint URLs."""
    if pictures is None:
        return []
    if not isinstance(pictures, list):
        return []

    resolved = []
    for picture in pictures:
        if isinstance(picture, str):
            resolved.append(_resolve_spot_image_endpoint_url(picture.strip(), current_spot=current_spot))
        else:
            resolved.append(picture)

    return normalize_picture_urls(resolved)


def _study_spot_from_json(data, spot=None):
    """Build or update StudySpot from request JSON. Returns (StudySpot, error_response)."""
    if spot is None:
        spot = StudySpot()
    """
    Build or update StudySpot from request JSON.

    Returns:
        tuple[StudySpot | None, tuple | None]: (spot, error_response)
        Exactly one element of the tuple will be non-None:
        - On success: (StudySpot instance, None)
        - On validation error: (None, (json_response, status_code))
    """
    if spot is None:
        spot = StudySpot()
    try:
        # Required fields
        if 'abbreviation' in data:
            spot.abbreviation = data['abbreviation']
        if 'study_spot_name' in data:
            spot.study_spot_name = data['study_spot_name']
        if 'address' in data:
            spot.address = data['address']
        if 'noise_level' in data:
            spot.noise_level = data['noise_level']
        if 'capacity' in data:
            spot.capacity = int(data['capacity'])
        if 'spot_type' in data:
            spot.spot_type = list(data['spot_type']) if data['spot_type'] is not None else []
        if 'access_hours' in data:
            spot.access_hours = _normalize_access_hours(data['access_hours'])
        if 'near_food' in data:
            spot.near_food = bool(data['near_food'])
        if 'reservable' in data:
            spot.reservable = bool(data['reservable'])
        if 'description' in data:
            spot.description = data['description']
        if 'pictures' in data:
            spot.pictures = _normalize_incoming_pictures(data['pictures'], current_spot=spot)
        # Optional
        if 'building_name' in data:
            spot.building_name = data['building_name'] if data['building_name'] else None
        if 'floor' in data:
            spot.floor = data['floor'] if data['floor'] is not None else None
        if 'tags' in data:
            spot.tags = list(data['tags']) if data['tags'] is not None else []
        if 'additional_properties' in data:
            spot.additional_properties = data['additional_properties'] if data['additional_properties'] else None
    except ValueError as exc:
        logger.warning(f"Invalid study spot data: {exc}")
        error_body = {
            'error': 'Invalid study spot data',
            'details': str(exc),
        }
        return None, (jsonify(error_body), 400)
    return spot, None


def _serialize_spot(spot):
    """Serialize a StudySpot with ID-based proxied image URLs."""
    payload = spot.to_dict()
    pictures = payload.get('pictures', [])
    payload['pictures'] = [
        _spot_image_endpoint_url(spot.id, index)
        for index in range(len(pictures))
    ]
    return payload


@api_bp.route('/image_proxy', methods=['GET'])
def image_proxy():
    """
    Proxy remote images so web clients can render DB image URLs reliably.
    Query param: ?url=<encoded-remote-image-url>
    """
    raw_url = (request.args.get('url') or '').strip()
    if not raw_url:
        return jsonify({'error': 'Missing url query parameter'}), 400
    proxied_response, errors = _proxy_image_from_remote_url(raw_url)
    if proxied_response is not None:
        return proxied_response

    logger.warning('Image proxy failed for %s. Attempts: %s', raw_url, ' | '.join(errors))
    return jsonify({'error': 'Failed to fetch image from upstream URL'}), 502


@api_bp.route('/study_spots/<int:spot_id>/images/<int:image_index>', methods=['GET'])
def get_study_spot_image(spot_id, image_index):
    """Fetch a study spot image by study spot ID and image index."""
    try:
        spot = StudySpot.query.get(spot_id)
        if spot is None:
            return jsonify({'error': 'Study spot not found'}), 404

        picture_url = _get_spot_picture_url_by_index(spot, image_index)
        if picture_url is None:
            return jsonify({'error': 'Image not found'}), 404

        proxied_response, errors = _proxy_image_from_remote_url(picture_url)
        if proxied_response is not None:
            return proxied_response

        logger.warning(
            'Study spot image proxy failed for spot_id=%s image_index=%s. Attempts: %s',
            spot_id,
            image_index,
            ' | '.join(errors),
        )
        return jsonify({'error': 'Failed to fetch study spot image'}), 502
    except Exception as e:
        logger.error(f"Error fetching study spot image spot_id={spot_id} image_index={image_index}: {str(e)}")
        return jsonify({'error': 'Failed to fetch study spot image'}), 500


# Study spot endpoints
@api_bp.route('/study_spots', methods=['GET'])
def get_study_spots():
    """
    Get all study spots.
    """
    try:
        spots = StudySpot.query.all()
        return jsonify([_serialize_spot(s) for s in spots]), 200
    except Exception as e:
        logger.error(f"Error fetching study spots: {str(e)}")
        return jsonify({'error': 'Failed to fetch study spots'}), 500


@api_bp.route('/study_spots/<int:spot_id>', methods=['GET'])
def get_study_spot(spot_id):
    """
    Get a single study spot by ID.
    """
    try:
        spot = StudySpot.query.get_or_404(spot_id)
        return jsonify(_serialize_spot(spot)), 200
    except Exception as e:
        logger.error(f"Error fetching study spot {spot_id}: {str(e)}")
        return jsonify({'error': 'Study spot not found'}), 404


@api_bp.route('/study_spots', methods=['POST'])
def create_study_spot():
    """
    Create a new study spot.
    JSON body must include: abbreviation, study_spot_name, address, noise_level,
    capacity, spot_type, access_hours, near_food, reservable, description, pictures.
    access_hours format:
    [["HH:MM", "HH:MM"], ...] for Monday->Sunday.
    Optional: building_name, floor, tags, additional_properties.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        missing = STUDY_SPOT_REQUIRED - set(data.keys())
        if missing:
            return jsonify({'error': f'Missing required fields: {sorted(missing)}'}), 400

        spot, err = _study_spot_from_json(data)
        if err:
            return err
        db.session.add(spot)
        db.session.commit()
        logger.info(f"Created study spot: {spot.study_spot_name} (ID: {spot.id})")
        return jsonify(_serialize_spot(spot)), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating study spot: {str(e)}")
        return jsonify({'error': 'Failed to create study spot'}), 500


@api_bp.route('/study_spots/<int:spot_id>', methods=['PUT'])
def update_study_spot(spot_id):
    """
    Update an existing study spot. Send only fields to update.
    """
    try:
        spot = StudySpot.query.get_or_404(spot_id)
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        spot, err = _study_spot_from_json(data, spot=spot)
        if err:
            return err
        db.session.commit()
        logger.info(f"Updated study spot: {spot.study_spot_name} (ID: {spot.id})")
        return jsonify(_serialize_spot(spot)), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating study spot {spot_id}: {str(e)}")
        return jsonify({'error': 'Failed to update study spot'}), 500


@api_bp.route('/study_spots/<int:spot_id>', methods=['DELETE'])
def delete_study_spot(spot_id):
    """
    Delete a study spot by ID.
    """
    try:
        spot = StudySpot.query.get_or_404(spot_id)
        name = spot.study_spot_name
        db.session.delete(spot)
        db.session.commit()
        logger.info(f"Deleted study spot: {name} (ID: {spot_id})")
        return jsonify({'message': 'Study spot deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting study spot {spot_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete study spot'}), 500
