import os
import pytest
import requests

from dotenv import load_dotenv

from entities.user import User
from constants.roles import Roles
from utils.data_generator import DataGenerator
from clients.auth.auth_api import AuthAPI
from clients.movies.movies_api import MoviesAPI
from db_models.db_helpers import get_movie_by_name_from_db

load_dotenv()

ADMIN_CREDENTIALS = {
    "email": os.environ["ADMIN_EMAIL"],
    "password": os.environ["ADMIN_PASSWORD"]
}


@pytest.fixture(scope="function")
def movies_api():
    """возвращает MoviesAPI с авторизацией """

    session = requests.Session()
    auth_api = AuthAPI(session=session)
    auth_api.login_user(ADMIN_CREDENTIALS)
    return MoviesAPI(session=session)


@pytest.fixture
def create_movie(super_admin):
    """Создает фильм под super admin перед тестом и потом удаляет его"""

    genre_id = super_admin.api.movies_api.get_genres()[0]["id"]
    movie_data = DataGenerator.generate_movie_data(genre_id)
    response = super_admin.api.movies_api.create_movie(movie_data)
    created_movie = response.json()

    yield created_movie

    super_admin.api.movies_api.delete_movie(created_movie["id"], expected_status=(200, 404))


@pytest.fixture
def movie_db_sync_data(super_admin):
    """Данные для теста синхронизации фильма с БД (жанр + данные фильма с уникальным name)"""

    genre_id = super_admin.api.movies_api.get_genres()[0]["id"]
    movie_data = DataGenerator.generate_movie_data(genre_id)

    yield movie_data, genre_id

    leftover = get_movie_by_name_from_db(movie_data["name"])
    if leftover is not None:
        super_admin.api.movies_api.delete_movie(leftover.id, expected_status=(200, 404))


@pytest.fixture
def creation_user_data():
    """Данные для создания новго пользователя через POST"""

    password = DataGenerator.generate_random_password()
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": [Roles.USER.value],
        "verified": True,
        "banned": False
    }


@pytest.fixture
def admin(user_session, super_admin):
    """
    Возвращает авторизованного пользователя с ролью ADMIN.
    Пользователя создаёт super_admin, затем admin аутентифицируется.
    """
    new_session = user_session()

    password = DataGenerator.generate_random_password()
    admin_data = {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": [Roles.ADMIN.value],
        "verified": True,
        "banned": False
    }

    admin_user = User(
        admin_data["email"],
        admin_data["password"],
        [Roles.ADMIN.value],
        new_session
    )

    super_admin.api.user_api.create_user(admin_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user
