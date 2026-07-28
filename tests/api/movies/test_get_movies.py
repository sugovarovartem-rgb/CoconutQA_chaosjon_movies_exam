import allure
import pytest

from models.movie_response import MoviesListResponseModel


@allure.epic("Cinescope Movies API")
@allure.feature("Получение списка фильмов (GET /movies)")
class TestGetMovies:
    """Тесты для GET /movies"""

    @allure.story("Получение списка фильмов без параметров")
    @allure.title("Список фильмов без параметров соответствует схеме ответа")
    @allure.description("Проверяем, что ответ без параметров содержит все ожидаемые поля пагинации.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_get_movies_without_params(self, super_admin):
        """Позитивный: запрос без параметров возвращает список фильмов по схеме"""
        with allure.step("Запросить список фильмов без параметров"):
            response = super_admin.api.movies_api.get_movies()
            body = response.json()

        with allure.step("Проверить схему ответа через pydantic-модель"):
            MoviesListResponseModel(**body)

    @allure.story("Фильтрация по жанру")
    @allure.title("Фильтрация по genreId возвращает только фильмы этого жанра")
    @allure.description("Проверяем, что все фильмы в ответе имеют переданный genreId.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.positive
    @pytest.mark.regression
    def test_get_movies_filter_by_genre_id(self, super_admin):
        """Позитивный: фильтрация по genreId - все фильмы имеют указанный genreId."""
        with allure.step("Получить genre_id из списка жанров"):
            genre_id = super_admin.api.movies_api.get_genres()[0]["id"]

        with allure.step("Запросить фильмы с фильтром по genreId"):
            response = super_admin.api.movies_api.get_movies(params={"genreId": genre_id})
            movies = response.json()["movies"]

        with allure.step("Проверить, что у всех фильмов совпадает genreId"):
            assert len(movies) > 0
            assert all(movie["genreId"] == genre_id for movie in movies)

    @allure.story("Фильтрация по локации")
    @allure.title("Фильтрация по locations возвращает только фильмы этой локации")
    @allure.description("Проверяем, что все фильмы в ответе имеют переданную локацию.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.positive
    @pytest.mark.regression
    def test_get_movies_filter_by_location(self, super_admin):
        """Позитивный: фильтрация по locations - все фильмы в указанной локации"""
        with allure.step("Запросить фильмы с фильтром locations=MSK"):
            response = super_admin.api.movies_api.get_movies(params={"locations": ["MSK"]})
            movies = response.json()["movies"]

        with allure.step("Проверить, что у всех фильмов локация MSK"):
            assert len(movies) > 0
            assert all(movie["location"] == "MSK" for movie in movies)

    @allure.story("Фильтрация по диапазону цен")
    @allure.title("Фильтрация по minPrice/maxPrice возвращает фильмы в диапазоне")
    @allure.description("Проверяем, что цена всех фильмов в ответе укладывается в заданный диапазон.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.positive
    @pytest.mark.regression
    def test_get_movies_filter_by_price_range(self, super_admin):
        """Позитивный: фильтрация по диапазону цен - все фильмы в диапазоне"""
        with allure.step("Запросить фильмы с фильтром по диапазону цен 100-300"):
            min_price, max_price = 100, 300
            response = super_admin.api.movies_api.get_movies(
                params={"minPrice": min_price, "maxPrice": max_price}
            )
            movies = response.json()["movies"]

        with allure.step("Проверить, что цена всех фильмов в диапазоне"):
            assert all(min_price <= movie["price"] <= max_price for movie in movies)

    @allure.story("Фильтрация по published")
    @allure.title("Фильтрация по published=False возвращает только неопубликованные фильмы")
    @allure.description("Проверяем, что все фильмы в ответе имеют published=False.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.positive
    @pytest.mark.regression
    def test_get_movies_filter_by_published(self, super_admin):
        """Позитивный: фильтрация по published=False - все фильмы неопубликованы"""
        with allure.step("Запросить фильмы с фильтром published=False"):
            response = super_admin.api.movies_api.get_movies(params={"published": False})
            movies = response.json()["movies"]

        with allure.step("Проверить, что все фильмы неопубликованы"):
            assert all(movie["published"] is False for movie in movies)

    @allure.story("Пагинация")
    @allure.title("Пагинация возвращает корректные page и pageSize")
    @allure.description(
        "Проверяем, что параметры page и pageSize отражаются в ответе, "
        "а размер списка не превышает pageSize."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.positive
    @pytest.mark.regression
    def test_get_movies_pagination(self, super_admin):
        """Позитивный: пагинация - размер списка не превышает pageSize - page совпадает"""
        with allure.step("Запросить вторую страницу с pageSize=5"):
            page_size = 5
            response = super_admin.api.movies_api.get_movies(
                params={"page": 2, "pageSize": page_size}
            )
            body = response.json()

        with allure.step("Проверить page, pageSize и размер списка"):
            assert body["page"] == 2
            assert body["pageSize"] == page_size
            assert len(body["movies"]) <= page_size

    @allure.story("Сортировка по дате создания")
    @allure.title("Сортировка createdAt=desc выдаёт фильмы по убыванию даты")
    @allure.description("Проверяем, что список фильмов отсортирован по дате создания по убыванию.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.positive
    @pytest.mark.regression
    def test_get_movies_sort_by_created_at_desc(self, super_admin):
        """Позитивный: сортировка по дате создания по убыванию"""
        with allure.step("Запросить фильмы с сортировкой createdAt=desc"):
            response = super_admin.api.movies_api.get_movies(
                params={"createdAt": "desc", "pageSize": 20}
            )
            movies = response.json()["movies"]

        with allure.step("Проверить, что даты отсортированы по убыванию"):
            dates = [movie["createdAt"] for movie in movies]
            assert dates == sorted(dates, reverse=True)

    @allure.story("Граница pageSize сверху")
    @allure.title("pageSize=20 (максимум) успешно обрабатывается")
    @allure.description("Проверяем граничное значение pageSize=20 - запрос должен пройти успешно.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.positive
    @pytest.mark.regression
    def test_get_movies_max_page_size_boundary(self, super_admin):
        """Граничный: pageSize=20 (максимум) - успешный"""
        with allure.step("Запросить фильмы с pageSize=20"):
            response = super_admin.api.movies_api.get_movies(params={"pageSize": 20})

        with allure.step("Проверить, что pageSize в ответе равен 20"):
            assert response.json()["pageSize"] == 20

    @allure.story("Граница pageSize сверху нарушена")
    @allure.title("pageSize=21 превышает максимум и возвращает 400")
    @allure.description("Проверяем, что значение pageSize выше максимума (20) отклоняется с 400.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_get_movies_page_size_above_limit(self, super_admin):
        """Негативный: pageSize=21 превышает максимум (20) - ожидаем 400"""
        with allure.step("Запросить фильмы с pageSize=21 - ожидаем 400"):
            super_admin.api.movies_api.get_movies(params={"pageSize": 21}, expected_status=400)

    @allure.story("Граница page снизу нарушена")
    @allure.title("page=0 меньше минимума и возвращает 400")
    @allure.description("Проверяем, что значение page ниже минимума (1) отклоняется с 400.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_get_movies_page_below_minimum(self, super_admin):
        """Негативный: page=0 меньше минимума (1) - 400"""
        with allure.step("Запросить фильмы с page=0 - ожидаем 400"):
            super_admin.api.movies_api.get_movies(params={"page": 0}, expected_status=400)

    @allure.story("Невалидное значение location в фильтре")
    @allure.title("Фильтр locations вне enum возвращает 400")
    @allure.description("Проверяем, что значение locations вне enum (MSK/SPB) отклоняется с 400.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_get_movies_invalid_location_value(self, super_admin):
        """Негативный: значение locations вне enum ("MSK"/"SPB") - 400"""
        with allure.step("Запросить фильмы с locations=NSK - ожидаем 400"):
            super_admin.api.movies_api.get_movies(params={"locations": ["NSK"]}, expected_status=400)
