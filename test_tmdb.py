import pytest
import tmdb_client
from unittest.mock import Mock
from main import app

def test_get_movies_list(monkeypatch):
   # Lista, którą będzie zwracać przysłonięte "zapytanie do API"
   mock_movies_list = ['Movie 1', 'Movie 2']

   requests_mock = Mock()
   # Wynik wywołania zapytania do API
   response = requests_mock.return_value
   # Przysłaniamy wynik wywołania metody .json()
   response.json.return_value = mock_movies_list
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)


   movies_list = tmdb_client.get_movies_list(list_type="popular")
   assert movies_list == mock_movies_list

def test_get_single_movie(monkeypatch):
   mock_movie = 'Movie1'

   request_mock = Mock()
   response = request_mock.return_value
   response.json.return_value = mock_movie

   monkeypatch.setattr('tmdb_client.requests.get', request_mock)
   movie = tmdb_client.get_single_movie(movie_id=1)
   assert movie == mock_movie

def test_get_movie_images(monkeypatch):
   mock_movie_images = 'Movie1'

   request_mock = Mock()
   response = request_mock.return_value
   response.json.return_value = mock_movie_images

   monkeypatch.setattr('tmdb_client.requests.get', request_mock)
   movie = tmdb_client.get_movie_images(movie_id=1)
   assert movie == mock_movie_images

def test_get_single_movie_cast(monkeypatch):
   mock_cast = [{'name': 'Actor1'}, {'name': 'Actor2'}]

   request_mock = Mock()
   response = request_mock.return_value
   response.json.return_value = {'cast': mock_cast}

   monkeypatch.setattr('tmdb_client.requests.get', request_mock)
   cast = tmdb_client.get_single_movie_cast(movie_id=1)
   assert cast == mock_cast

@pytest.mark.parametrize('list_type', [
   'popular',
   'top_rated', 
   'now_playing', 
   'upcoming'
   ])
def test_homepage(monkeypatch, list_type):
    api_mock = Mock(return_value={'results': []})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get(f'/?list_type={list_type}')
        assert response.status_code == 200
        api_mock.assert_called_with(f'movie/{list_type}')

