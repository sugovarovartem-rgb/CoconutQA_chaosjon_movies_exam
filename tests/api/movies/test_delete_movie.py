import requests

from clients.movies.movies_api import MoviesAPI
from utils.data_generator import DataGenerator


class TestDeleteMovie:
    """тесты для delete - удаление фильма"""

    def test_delete_movie_success(self, movies_api):
        """удаление существуюющего фильма"""

        genre_id = movies_api.get_genres()[0]["id"]
        movie_data = DataGenerator.generate_movie_data(genre_id)
        created_movie = movies_api.create_movie(movie_data).json()
        response = movies_api.delete_movie(created_movie["id"])
        assert response.json()["id"] == created_movie["id"]
        movies_api.get_movie_by_id(created_movie["id"], expected_status=404)

    def test_delete_movie_twice(self, movies_api):
        """негативный. повторное удаление уже удаленного фильма - 404"""

        genre_id = movies_api.get_genres()[0]["id"]
        movie_data = DataGenerator.generate_movie_data(genre_id)
        created_movie = movies_api.create_movie(movie_data).json()

        movies_api.delete_movie(created_movie["id"])
        movies_api.delete_movie(created_movie["id"], expected_status=404)

    def test_delete_nonexistent_movie(self, movies_api):
        """негативный, удаление несуществующего id - 404"""

        nonexistent_id = 999999999
        movies_api.delete_movie(nonexistent_id, expected_status=404)

    def test_delete_movie_without_auth(self, movies_api, create_movie):
        """негативный, удаление без авторизации - 400"""

        anonymous_session = requests.Session()
        anonymous_movies_api = MoviesAPI(session=anonymous_session)
        anonymous_movies_api.delete_movie(
            create_movie["id"], expected_status=401)
