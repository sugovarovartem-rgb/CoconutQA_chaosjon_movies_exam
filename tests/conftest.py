import pytest
import requests

from api.api_manager import ApiManager
from entities.user import User
from resources.user_creds import SuperAdminCreds
from constants.roles import Roles
from utils.data_generator import DataGenerator


@pytest.fixture
def user_session():
    """Возвращает функцию, которая создает новый ApiManager"""

    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session_manager = ApiManager(session)
        user_pool.append(user_session_manager)
        return user_session_manager

    yield _create_user_session

    for manager in user_pool:
        manager.close_session()

@pytest.fixture
def super_admin(user_session):
    """Возвращает авторизованного пользователя с ролью SUPER ADMIN"""

    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    """Возвращает авторизованного пользователя с ролью USER"""

    new_session = user_session()

    common_user = User(
        creation_user_data["email"],
        creation_user_data["password"],
        [Roles.USER.value],
        new_session
    )
    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user