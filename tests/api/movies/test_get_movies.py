class TestGetMovies:

    # гет тесты - получение афиши фильмов с фильтрацией

    def test_get_movies_without_params(self, movies_api):
        response = movies_api.get_movies()
        body = response.json()
        assert "movies" in body
        assert "count" in body
        assert "page" in body
        assert "pageSize" in body
        assert "pageCount" in body
        assert isinstance(body["movies"], list)

    def test_get_movies_filter_by_genre_id(self, movies_api):
        genre_id = movies_api.get_genres()[0]["id"]
        response = movies_api.get_movies(params={"genreId": genre_id})
        movies = response.json()["movies"]
        assert len(movies) > 0
        assert all(movie["genreId"] == genre_id for movie in movies)

    def test_get_movies_filter_by_location(self, movies_api):
        response = movies_api.get_movies(params={"locations": ["MSK"]})
        movies = response.json()["movies"]
        assert len(movies) > 0
        assert all(movie["location"] == "MSK" for movie in movies)

    def test_get_movies_filter_by_price_range(self, movies_api):
        min_price, max_price = 100, 300
        response = movies_api.get_movies(
            params={
                "minPrice": min_price,
                "maxPrice": max_price})
        movies = response.json()["movies"]
        assert all(min_price <= movie["price"] <=
                   max_price for movie in movies)

    def test_get_movies_filter_by_published(self, movies_api):
        response = movies_api.get_movies(params={"published": False})
        movies = response.json()["movies"]
        assert all(movie["published"] is False for movie in movies)

    def test_get_movies_pagination(self, movies_api):
        page_size = 5

        response = movies_api.get_movies(
            params={"page": 2, "pageSize": page_size})
        body = response.json()
        assert body["page"] == 2
        assert body["pageSize"] == page_size
        assert len(body["movies"]) <= page_size

    def test_get_movies_sort_by_created_at_desc(self, movies_api):
        response = movies_api.get_movies(
            params={"createdAt": "desc", "pageSize": 20})
        movies = response.json()["movies"]
        dates = [movie["createdAt"] for movie in movies]
        assert dates == sorted(dates, reverse=True)

    def test_get_movies_max_page_size_boundary(self, movies_api):
        response = movies_api.get_movies(params={"pageSize": 20})
        assert response.json()["pageSize"] == 20

    def test_get_movies_page_size_above_limit(self, movies_api):
        movies_api.get_movies(params={"pageSize": 21}, expected_status=400)

    def test_get_movies_page_below_minimum(self, movies_api):
        movies_api.get_movies(params={"page": 0}, expected_status=400)

    def test_get_movies_invalid_location_value(self, movies_api):
        movies_api.get_movies(
            params={
                "locations": ["NSK"]},
            expected_status=400)
