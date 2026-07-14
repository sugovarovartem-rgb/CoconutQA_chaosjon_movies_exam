from custom_requester.custom_requester import CustomRequester
from constants import LOGIN_ENDPOINT, REGISTER_ENDPOINT
from enums.hosts import Hosts

class AuthAPI(CustomRequester):
    """класс для работы с аутентификацией"""

    def __init__(self, session):
        super().__init__(session=session, base_url=Hosts.AUTH_URL.value)

    def register_user(self, user_data, expected_status=201):
        """регистрация новго пользователя"""

        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, login_data, expected_status=(200, 201)):
        """авторизация пользователя"""

        response = self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )
        access_token = response.json()["accessToken"]
        self._update_session_headers(Authorization=f"Bearer {access_token}")
        return response
