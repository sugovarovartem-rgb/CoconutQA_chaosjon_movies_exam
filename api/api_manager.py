import requests

from clients.auth.auth_api import AuthAPI
from clients.movies.movies_api import MoviesAPI
from clients.user.user_api import UserAPI


class ApiManager:
    """Объединяет все API- клиенты на одной общей сессии requests"""

    def __init__(self, session: requests.Session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.movies_api = MoviesAPI(session)
        self.user_api = UserAPI(session)


    def close_session(self):
        """Закрывает сессию. Вызывается фикстурой после теста"""
        self.session.close()