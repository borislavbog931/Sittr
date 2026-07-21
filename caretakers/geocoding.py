import json
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


def geocode_city(city):
    """Look up (lat, lng) for a city name via the Google Geocoding API.

    Returns None on any failure (missing key, network error, no match) so
    callers can save a Caretaker without coordinates rather than crash.

    Uses urllib instead of the third-party `requests` package because this
    project also has a local Django app named `requests` (for hire
    requests) that shadows it on import.
    """
    api_key = settings.GOOGLE_MAPS_API_KEY
    if not api_key or not city:
        return None

    query = urllib.parse.urlencode({"address": city, "key": api_key})
    url = f"{GEOCODE_URL}?{query}"

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, ValueError):
        return None

    if data.get("status") != "OK" or not data.get("results"):
        return None

    location = data["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]
