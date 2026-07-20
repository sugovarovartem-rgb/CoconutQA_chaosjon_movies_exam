import requests

from clients.movies.movies_api import MoviesAPI


class TestEditMovie:
    """тесты для patch - редактирование фильма"""

    def test_edit_movie_single_field(self, movies_api, create_movie):
        """обновление одного поля price"""

        new_price = 555
        response = movies_api.edit_movie(
            create_movie["id"], {"price": new_price})
        body = response.json()
        assert body["price"] == new_price
        assert body["name"] == create_movie["name"]
        assert body["location"] == create_movie["location"]

    def test_edit_movie_multiple_fields(self, movies_api, create_movie):
        """обновление нескольких полей сразу"""

        update_data = {
            "price": 777,
            "description": "Обновлённое описание",
            "published": False
        }
        response = movies_api.edit_movie(create_movie["id"], update_data)
        body = response.json()
        assert body["price"] == update_data["price"]
        assert body["description"] == update_data["description"]
        assert body["published"] == update_data["published"]

    def test_edit_nonexistent_movie(self, movies_api):
        """негативный, редактирование несуществующего id - 400"""

        nonexistent_id = 999999999
        movies_api.edit_movie(
            nonexistent_id, {
                "price": 100}, expected_status=404)

    def test_edit_movie_without_auth(self, create_movie):
        """негативный, редактивароние без авторизации - 400"""

        anonymous_session = requests.Session()
        anonymous_movies_api = MoviesAPI(session=anonymous_session)
        anonymous_movies_api.edit_movie(
            create_movie["id"], {"price": 100}, expected_status=401
        )

    def test_edit_movie_invalid_location(self, movies_api, create_movie):
        """негативный, location вне enum - 400"""

        movies_api.edit_movie(
            create_movie["id"], {"location": "NSK"}, expected_status=400
        )
