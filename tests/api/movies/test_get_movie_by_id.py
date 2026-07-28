import allure
import pytest

from models.movie_response import MovieResponseModel


@allure.epic("Cinescope Movies API")
@allure.feature("Получение фильма по id (GET /movies/{id})")
class TestGetMovieById:
    """Тесты для GET, Получение фильма по идентификатору"""

    @allure.story("Успешное получение фильма по id")
    @allure.title("Получение существующего фильма по id возвращает совпадающие поля")
    @allure.description("Проверяем, что поля ответа GET /movies/{id} совпадают с данными созданного фильма.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_get_movie_by_id_success(self, super_admin, create_movie):
        """Позитивный: получение существующего фильма по id - поля совпадают"""
        with allure.step("Запросить фильм по id"):
            response = super_admin.api.movies_api.get_movie_by_id(create_movie["id"])
            body = response.json()

        with allure.step("Проверить схему ответа через pydantic-модель"):
            MovieResponseModel(**body)

        with allure.step("Проверить, что поля ответа совпадают с данными созданного фильма"):
            assert body["id"] == create_movie["id"]
            assert body["name"] == create_movie["name"]
            assert body["price"] == create_movie["price"]
            assert body["genreId"] == create_movie["genreId"]

    @allure.story("Поле reviews в ответе")
    @allure.title("Ответ по фильму содержит поле reviews в виде списка")
    @allure.description("Проверяем, что ответ по конкретному фильму содержит поле reviews и это список.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.positive
    @pytest.mark.regression
    def test_get_movie_by_id_contains_reviews_field(self, super_admin, create_movie):
        """Позитивный: ответ по конкретному фильму содержит поле reviews"""
        with allure.step("Запросить фильм по id"):
            response = super_admin.api.movies_api.get_movie_by_id(create_movie["id"])
            body = response.json()

        with allure.step("Проверить наличие и тип поля reviews"):
            assert "reviews" in body
            assert isinstance(body["reviews"], list)

    @allure.story("Запрос несуществующего фильма")
    @allure.title("Запрос фильма с несуществующим id возвращает 404")
    @allure.description("Проверяем, что запрос по заведомо несуществующему id возвращает 404.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_get_movie_by_nonexistent_id(self, super_admin):
        """Негативный: запрос несуществующего id - ожидаем 404"""
        with allure.step("Запросить фильм с несуществующим id - ожидаем 404"):
            nonexistent_id = 999999999
            super_admin.api.movies_api.get_movie_by_id(nonexistent_id, expected_status=404)
