from custom_requester.custom_requester import CustomRequester
from constants.endpoints import MOVIES_ENDPOINT
from enums.hosts import Hosts


class MoviesAPI(CustomRequester):
    """
    класс для работы с фильмами
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=Hosts.MOVIES_URL.value)

    def get_movies(self, params=None, expected_status=200):
        """получение списка фильмов"""

        return self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            params=params,
            expected_status=expected_status
        )

    def get_movie_by_id(self, movie_id, expected_status=200):
        """получение фильма по идентификатору"""

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

        response = self.send_request(
            method="GET",
            endpoint="/genres",
            expected_status=expected_status
        )
        return response.json()

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
