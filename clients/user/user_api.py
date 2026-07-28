from custom_requester.custom_requester import CustomRequester
from constants.endpoints import USER_ENDPOINT
from enums.hosts import Hosts


class UserAPI(CustomRequester):
    """Класс для работы с пользователями (user на quth-сервисе"""

    def __init__(self, session):
        super().__init__(session=session, base_url=Hosts.AUTH_URL.value)

    def create_user(self, user_data, expected_status=201):
        """Создание пользователя"""

        return self.send_request(
            method="POST",
            endpoint=USER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def get_user(self, user_id_or_email, expected_status=200):
        """Получение пользователя по id или email"""

        endpoint = f"{USER_ENDPOINT}/{user_id_or_email}"
        return self.send_request(
            method="GET",
            endpoint=endpoint,
            expected_status=expected_status
        )