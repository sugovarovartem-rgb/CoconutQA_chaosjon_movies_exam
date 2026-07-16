import logging

import requests


class CustomRequester:

    """все апи клиенты наследуются от этого класса"""

    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.session.headers.update(self.headers)

    def send_request(self, method, endpoint, data=None, params=None, expected_status=200, need_logging=True):
        if params:
            params = {
                key: (str(value).lower() if isinstance(value, bool) else value)
                for key, value in params.items()
            }

        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, json=data, params=params, headers=self.headers)
        if need_logging:
            self.log_request_and_response(response)

        allowed_statuses = expected_status if isinstance(expected_status, (list, tuple)) else [expected_status]
        if response.status_code not in allowed_statuses:
            raise ValueError(
                f"Unexpected status code: {response.status_code}. Expected one of: {allowed_statuses}. "
                f"Response body: {response.text}"
            )
        return response

    def _update_session_headers(self, **kwargs):
        """обновление заголовков сессии"""

        self.headers.update(kwargs)
        self.session.headers.update(self.headers)

    @staticmethod
    def log_request_and_response(response):
        """логирование запроса и ответа """

        logging.info(
            f"Request: {response.request.method} {response.request.url}")
        if response.request.body:
            logging.info(f"Request body: {response.request.body}")
        logging.info(f"Response status: {response.status_code}")
        try:
            logging.info(f"Response body: {response.json()}")
        except ValueError:
            logging.info(f"Response body: {response.text}")
