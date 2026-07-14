from utils.data_generator import DataGenerator  # импорт


class TestCreateMovie:
    """тесты для post - создание фильма"""

    def test_create_movie_success(self, movies_api):
        """создание фильма с валидными данными"""

        genre_id = movies_api.get_genres().json()[0]["id"]
        movie_data = DataGenerator.generate_movie_data(genre_id)
        response = movies_api.create_movie(movie_data)
        body = response.json()
        assert response.status_code == 201
        assert body["name"] == movie_data["name"]
        assert body["price"] == movie_data["price"]
        assert body["location"] == movie_data["location"]
        assert body["genreId"] == genre_id
        assert "id" in body
        assert "createdAt" in body
        assert "genre" in body

        # подчищаем за собой
        movies_api.delete_movie(body["id"], expected_status=(200, 404))

    def test_create_movie_without_auth(self):
        """негативный, создание фильма без авторизации"""

        import requests
        from clients.movies.movies_api import MoviesAPI
        anonymous_session = requests.Session()
        anonymous_movies_api = MoviesAPI(session=anonymous_session)
        genre_id = anonymous_movies_api.get_genres().json()[0]["id"]
        movie_data = DataGenerator.generate_movie_data(genre_id)
        response = anonymous_movies_api.create_movie(
            movie_data, expected_status=401)
        assert response.status_code == 401

    def test_create_movie_missing_required_field(self, movies_api):
        """негативный, отсуствует обязательное поле name"""

        genre_id = movies_api.get_genres().json()[0]["id"]
        movie_data = DataGenerator.generate_movie_data(genre_id)
        del movie_data["name"]
        response = movies_api.create_movie(movie_data, expected_status=400)
        assert response.status_code == 400

    def test_create_movie_invalid_location(self, movies_api):
        """негативный, значение location вне (MSK/SPB)"""

        genre_id = movies_api.get_genres().json()[0]["id"]
        movie_data = DataGenerator.generate_movie_data(genre_id)
        movie_data["location"] = "NSK"
        response = movies_api.create_movie(movie_data, expected_status=400)
        assert response.status_code == 400

    def test_create_movie_duplicate_name(self, movies_api):
        """негативный, создание фильма с существующим name"""

        genre_id = movies_api.get_genres().json()[0]["id"]
        movie_data = DataGenerator.generate_movie_data(genre_id)
        first_response = movies_api.create_movie(movie_data)
        created_id = first_response.json()["id"]
        try:
            duplicate_response = movies_api.create_movie(
                movie_data, expected_status=409)
            assert duplicate_response.status_code == 409
        finally:
            movies_api.delete_movie(created_id, expected_status=(200, 404))
