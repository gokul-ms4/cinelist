import os
import time
import requests
from requests.exceptions import RequestException

API_KEY = os.environ.get("TMDB_API_KEY")  # set this in your environment / .env file
BASE_URL = 'https://api.themoviedb.org/3'


def _get_with_retry(url, params, max_retries=4, backoff=0.6, timeout=6):
    """Calls the TMDB API, retrying on failure before giving up."""
    last_exception = None
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except (RequestException, ValueError) as e:
            last_exception = e
            if attempt < max_retries - 1:
                time.sleep(backoff * (attempt + 1))  # 0.6s, 1.2s, 1.8s
    # all attempts failed — raise so the view can handle it
    raise last_exception


def get_popular_movies():
    url = f"{BASE_URL}/movie/popular"
    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }
    data = _get_with_retry(url, params)
    return data.get('results', [])


def search_movies(query):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": query,
        "language": "en-US"
    }
    data = _get_with_retry(url, params)
    return data.get('results', [])

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY}
    return _get_with_retry(url, params)


def get_movie_credits(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits"
    params = {"api_key": API_KEY}
    return _get_with_retry(url, params)