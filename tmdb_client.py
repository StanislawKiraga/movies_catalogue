import requests
import random
import os

API_TOKEN = os.environ.get('TMDB_API_TOKEN', '')

def call_tmdb_api(endpoint):
   full_url = f"https://api.themoviedb.org/3/{endpoint}"
   headers = {
       "Authorization": f"Bearer {API_TOKEN}"
   }
   response = requests.get(full_url, headers=headers)
   response.raise_for_status()
   return response.json()

def get_movies_list(list_type):
    return call_tmdb_api(f'movie/{list_type}')
   

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
    else:
        data = get_movies_list('popular')
    random.shuffle (data['results'])
    return data['results'][:how_many]

def get_single_movie(movie_id):
    return call_tmdb_api(f'movie/{movie_id}')
    

def get_single_movie_cast(movie_id):
    return call_tmdb_api(f'movie/{movie_id}/credits')['cast']
   

def get_movie_images(movie_id):
    return call_tmdb_api(f'movie/{movie_id}/images')
    