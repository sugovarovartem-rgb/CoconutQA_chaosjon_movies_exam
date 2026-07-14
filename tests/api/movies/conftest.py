import pytest
import requests

from clients.auth.auth_api import AuthAPI
from clients.movies.movies_api import MoviesAPI
from utils.data_generator import DataGenerator

ADMIN_CREDENTIALS = {
    "email": "api1@gmail.com",
    "password": "asdqwe123Q"
}


@pytest.fixture(scope="function")
def movies_api():
    """возвращает MoviesAPI с авторизацией """

    session = requests.Session()
    auth_api = AuthAPI(session=session)
    auth_api.login_user(ADMIN_CREDENTIALS)
    return MoviesAPI(session=session)


@pytest.fixture(scope="function")
def create_movie(movies_api):
    """создаем фильм перед тестом и потом удаляем его"""

    genre_id = movies_api.get_genres().json()[0]["id"]
    movie_data = DataGenerator.generate_movie_data(genre_id)
    response = movies_api.create_movie(movie_data)
    created_movie = response.json()

    yield created_movie

    movies_api.delete_movie(created_movie["id"], expected_status=(200, 404))
