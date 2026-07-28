import allure
import pytest

from models.movie_response import MovieResponseModel
from utils.data_generator import DataGenerator


@allure.epic("Cinescope Movies API")
@allure.feature("Создание фильма (POST /movies)")
class TestCreateMovie:
    """Тесты для POST /movies - создание фильма"""

    @allure.story("Успешное создание фильма")
    @allure.title("Супер админ создаёт фильм с валидными данными")
    @allure.description(
        "Проверяем, что супер админ может создать фильм с валидными данными "
        "и в ответе возвращаются все ожидаемые поля."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_create_movie_success(self, super_admin):
        """Позитивный: супер админ создаёт фильм с валидными данными."""
        with allure.step("Получить genre_id и сгенерировать данные фильма"):
            genre_id = super_admin.api.movies_api.get_genres()[0]["id"]
            movie_data = DataGenerator.generate_movie_data(genre_id)

        with allure.step("Создать фильм через POST /movies"):
            response = super_admin.api.movies_api.create_movie(movie_data)
            body = response.json()

        with allure.step("Проверить схему ответа через pydantic-модель"):
            MovieResponseModel(**body)

        with allure.step("Проверить, что тело ответа соответствует отправленным данным"):
            assert body["name"] == movie_data["name"]
            assert body["price"] == movie_data["price"]
            assert body["location"] == movie_data["location"]
            assert body["genreId"] == genre_id

        with allure.step("Удалить созданный фильм (уборка за тестом)"):
            super_admin.api.movies_api.delete_movie(body["id"], expected_status=(200, 404))

    @allure.story("Создание фильма без авторизации")
    @allure.title("Создание фильма анонимным пользователем возвращает 401")
    @allure.description("Проверяем, что без авторизации создать фильм нельзя.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_create_movie_without_auth(self, user_session):
        """Негативный: создание фильма без авторизации - 401"""
        with allure.step("Создать анонимную сессию и сгенерировать данные фильма"):
            anonymous = user_session()
            genre_id = anonymous.movies_api.get_genres()[0]["id"]
            movie_data = DataGenerator.generate_movie_data(genre_id)

        with allure.step("Попытаться создать фильм без авторизации - ожидаем 401"):
            anonymous.movies_api.create_movie(movie_data, expected_status=401)

    @allure.story("Создание фильма с отсутствующим обязательным полем")
    @allure.title("Создание фильма без поля name возвращает 400")
    @allure.description("Проверяем валидацию обязательного поля name при создании фильма.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_create_movie_missing_required_field(self, super_admin):
        """Негативный: отсутствует обязательное поле name - 400"""
        with allure.step("Сгенерировать данные фильма и удалить обязательное поле name"):
            genre_id = super_admin.api.movies_api.get_genres()[0]["id"]
            movie_data = DataGenerator.generate_movie_data(genre_id)
            del movie_data["name"]

        with allure.step("Попытаться создать фильм без поля name - ожидаем 400"):
            super_admin.api.movies_api.create_movie(movie_data, expected_status=400)

    @allure.story("Создание фильма с невалидным location")
    @allure.title("Создание фильма с location вне enum возвращает 400")
    @allure.description("Проверяем валидацию поля location при создании фильма.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_create_movie_invalid_location(self, super_admin):
        """Негативный: значение location вне enum - 400"""
        with allure.step("Сгенерировать данные фильма с невалидным location"):
            genre_id = super_admin.api.movies_api.get_genres()[0]["id"]
            movie_data = DataGenerator.generate_movie_data(genre_id)
            movie_data["location"] = "NSK"

        with allure.step("Попытаться создать фильм с невалидным location - ожидаем 400"):
            super_admin.api.movies_api.create_movie(movie_data, expected_status=400)

    @allure.story("Создание фильма с дублирующимся name")
    @allure.title("Повторное создание фильма с тем же name возвращает 409")
    @allure.description("Проверяем уникальность поля name при создании фильма.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_create_movie_duplicate_name(self, super_admin):
        """Негативный: создание фильма с уже существующим name - 409"""
        with allure.step("Создать фильм с уникальным name"):
            genre_id = super_admin.api.movies_api.get_genres()[0]["id"]
            movie_data = DataGenerator.generate_movie_data(genre_id)

            first_response = super_admin.api.movies_api.create_movie(movie_data)
            created_id = first_response.json()["id"]

        try:
            with allure.step("Повторно создать фильм с тем же name - ожидаем 409"):
                super_admin.api.movies_api.create_movie(movie_data, expected_status=409)
        finally:
            with allure.step("Удалить созданный фильм (уборка за тестом)"):
                super_admin.api.movies_api.delete_movie(created_id, expected_status=(200, 404))
