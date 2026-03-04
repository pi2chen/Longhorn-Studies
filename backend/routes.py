from flask import Blueprint, request, jsonify
from database import db
from sqlalchemy import inspect
from models import StudySpot
from datetime import datetime
import logging
import re

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

@api_bp.route('/schema', methods=['GET'])
def get_schema():
    """Return database schema information."""
    try:
        # Get all tables
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        schema = {}
        for table in tables:
            columns = inspector.get_columns(table)
            schema[table] = {
                'columns': [
                    {
                        'name': col['name'],
                        'type': str(col['type']),
                        'nullable': col['nullable'],
                        'default': str(col['default']) if col['default'] is not None else None
                    }
                    for col in columns
                ]
            }
        
        return jsonify(schema), 200
    except Exception as e:
        logger.error(f"Error getting schema: {str(e)}")
        return jsonify({'error': 'Failed to get schema'}), 500

@api_bp.route('/study_spots/raw', methods=['GET'])
def get_raw_study_spots():
    """Return raw StudySpot data as-is from database."""
    try:
        spots = StudySpot.query.all()
        return jsonify([s.to_dict() for s in spots]), 200
    except Exception as e:
        logger.error(f"Error fetching raw study spots: {str(e)}")
        return jsonify({'error': 'Failed to fetch study spots'}), 500

@api_bp.route('/study_spots/distinct/<column>', methods=['GET'])
def get_distinct_values(column):
    try: 
        allowed_columns = {'spot_type', 'noise_level', 'tags', 'access_hours'}
        if column not in allowed_columns:
            return jsonify({'error': 'Invalid column name'}), 400
        
        if column == 'access_hours':
            # For open now, return boolean options as JSON booleans
            return jsonify([True, False]), 200
        elif column in {'spot_type', 'tags'}:
            # Handle JSON arrays
            spots = StudySpot.query.all()
            values = set()
            for spot in spots:
                col_data = getattr(spot, column)
                if col_data: 
                    for item in col_data:
                        if item:
                            values.add(str(item))
        else: 
            # Handle regular string columns
            values = db.session.query(getattr(StudySpot, column)).distinct().all()
            values = [v[0] for v in values if v[0] is not None]

        return jsonify(sorted(list(values))), 200
    except Exception as e:
        logger.error(f"Error fetching distinct values for column {column}: {str(e)}")
        return jsonify({'error': 'Failed to fetch distinct values'}), 500

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
            spot.pictures = list(data['pictures']) if data['pictures'] is not None else []
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


# Study spot endpoints
@api_bp.route('/study_spots', methods=['GET'])
def get_study_spots():
    """
    Get all study spots.
    """
    try:
        spots = StudySpot.query.all()
        return jsonify([s.to_dict() for s in spots]), 200
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
        return jsonify(spot.to_dict()), 200
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
        return jsonify(spot.to_dict()), 201
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
        return jsonify(spot.to_dict()), 200
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
