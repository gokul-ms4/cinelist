import requests

API_KEY = 'faecc784db46297338de9a2cec3b7cc2'

BASE_URL = 'https://api.themoviedb.org/3'

def get_popular_movies():

    url = f"{BASE_URL}/movie/popular"

    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    response = requests.get(url, params=params)

    return response.json().get('results', [])

def search_movies(query):

    url = f"{BASE_URL}/search/movie"

    params = {
        "api_key": API_KEY,
        "query": query,
        "language": "en-US"
    }

    response = requests.get(url, params=params)
    
    return response.json().get('results', [])
