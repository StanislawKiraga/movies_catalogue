import requests
import random

API_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwYWZmNDgzMGViMDY4NDRhNWIwMWQyMDNjYzJhNzkyNiIsInN1YiI6IjY0MmMzMjM3OGRlMGFlMDExMzUxMWEzMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.w8oqRme7VJA9ccPaCAlXXrIN68m2jZl5vN-nsTDGzPc'


def get_movies_list(list_type):
    endpoint = f"https://api.themoviedb.org/3/movie/{list_type}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()

def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"

def get_movies(how_many, list_type):
    if list_type == 'popular':
        data = get_movies_list('popular')
    elif list_type == 'top_rated':
        data =  get_movies_list('top_rated')
    elif list_type == 'upcoming':
        data =  get_movies_list('upcoming')
    elif list_type == 'now_playing':
        data =  get_movies_list('now_playing')
    random.shuffle (data['results'])
    return data['results'][:how_many]

def get_single_movie(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()

def get_single_movie_cast(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()["cast"]

def get_movie_images(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()