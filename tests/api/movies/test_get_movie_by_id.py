class TestGetMovieById:
    """получение фильма по идентификатору"""

    def test_get_movie_by_id_success(self, movies_api, create_movie):
        """получение существующего фильма"""

        response = movies_api.get_movie_by_id(create_movie["id"])
        body = response.json()
        assert body["id"] == create_movie["id"]
        assert body["name"] == create_movie["name"]
        assert body["price"] == create_movie["price"]
        assert body["genreId"] == create_movie["genreId"]

    def test_get_movie_by_id_contains_reviews_field(
            self, movies_api, create_movie):
        """ответ по конкретному фильму, поле reviews"""

        response = movies_api.get_movie_by_id(create_movie["id"])
        body = response.json()
        assert "reviews" in body
        assert isinstance(body["reviews"], list)

    def test_get_movie_by_nonexistent_id(self, movies_api):
        """негативный, несуществующий id """

        nonexistent_id = 999999999
        response = movies_api.get_movie_by_id(
            nonexistent_id, expected_status=404)
        assert response.status_code == 404
