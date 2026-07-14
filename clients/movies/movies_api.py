from urllib.parse import urlencode

from custom_requester.custom_requester import CustomRequester
from constants import MOVIES_ENDPOINT
from enums.hosts import Hosts


class MoviesAPI(CustomRequester):
    """класс для работы с фильмами"""

    def __init__(self, session):
        super().__init__(session=session, base_url=Hosts.MOVIES_URL.value)

    def get_movies(self, params=None, expected_status=200):
        """получение списка фильмов"""

        endpoint = MOVIES_ENDPOINT
        if params:
            normalized_params = {
                key: (str(value).lower() if isinstance(value, bool) else value)
                for key, value in params.items()
            }
            query_string = urlencode(normalized_params, doseq=True)
            endpoint = f"{MOVIES_ENDPOINT}?{query_string}"
        return self.send_request(
            method="GET",
            endpoint=endpoint,
            expected_status=expected_status
        )

    def get_movie_by_id(self, movie_id, expected_status=200):
        """получение фильма по индтефикатору"""

        endpoint = f"{MOVIES_ENDPOINT}/{movie_id}"
        return self.send_request(
            method="GET",
            endpoint=endpoint,
            expected_status=expected_status
        )

    def create_movie(self, movie_data, expected_status=201):
        """создание фильма"""

        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )

    def get_genres(self, expected_status=200):
        """получение списка жанров"""

        return self.send_request(
            method="GET",
            endpoint="/genres",
            expected_status=expected_status
        )

    def edit_movie(self, movie_id, movie_data, expected_status=200):
        "редактирование фильма"

        endpoint = f"{MOVIES_ENDPOINT}/{movie_id}"
        return self.send_request(
            method="PATCH",
            endpoint=endpoint,
            data=movie_data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        """удаление фильма"""

        endpoint = f"{MOVIES_ENDPOINT}/{movie_id}"
        return self.send_request(
            method="DELETE",
            endpoint=endpoint,
            expected_status=expected_status
        )
