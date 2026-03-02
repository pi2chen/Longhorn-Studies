from urllib.parse import parse_qs, urlparse
import re


DRIVE_FILE_PATH_RE = re.compile(r"/file/d/([A-Za-z0-9_-]+)")
IMAGE_PROXY_PATH_SUFFIX = "/api/image_proxy"


def _unwrap_image_proxy_once(url):
    """If URL is our image proxy endpoint, return the nested source URL."""
    parsed = urlparse(url)
    path = (parsed.path or "").rstrip("/")
    if not path.endswith(IMAGE_PROXY_PATH_SUFFIX):
        return url

    nested = parse_qs(parsed.query or "").get("url", [None])[0]
    if isinstance(nested, str):
        nested = nested.strip()
        if nested:
            return nested

    return url


def _unwrap_image_proxy_url(url):
    """Unwrap up to 3 nested proxy URLs."""
    current = url
    for _ in range(3):
        unwrapped = _unwrap_image_proxy_once(current)
        if unwrapped == current:
            break
        current = unwrapped
    return current


def _extract_google_drive_file_id(url):
    """Extract a Google Drive file id from common public share URL formats."""
    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower()

    if "drive.google.com" not in hostname and "docs.google.com" not in hostname:
        return None

    path_match = DRIVE_FILE_PATH_RE.search(parsed.path or "")
    if path_match:
        return path_match.group(1)

    query_params = parse_qs(parsed.query or "")
    file_id = query_params.get("id", [None])[0]
    if file_id:
        return file_id

    return None


def normalize_google_drive_url(url):
    """
    Convert Google Drive share URLs into a direct image URL.
    Returns the input URL unchanged if no Drive file id is found.
    """
    if not isinstance(url, str):
        return url

    url = url.strip()
    if not url:
        return url

    # If a proxied URL is passed back from clients, keep DB storage canonical.
    url = _unwrap_image_proxy_url(url)

    file_id = _extract_google_drive_file_id(url)
    if not file_id:
        return url

    return f"https://drive.google.com/uc?export=view&id={file_id}"


def normalize_picture_urls(pictures):
    """
    Normalize a list of image URLs for mobile-friendly rendering.
    """
    if pictures is None:
        return []
    if not isinstance(pictures, list):
        return []

    return [normalize_google_drive_url(url) for url in pictures]
