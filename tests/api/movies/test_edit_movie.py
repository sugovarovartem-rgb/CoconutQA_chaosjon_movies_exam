import allure
import pytest


@allure.epic("Cinescope Movies API")
@allure.feature("Редактирование фильма (PATCH /movies/{id})")
class TestEditMovie:
    """Тесты для PATCH - редактирование фильма"""

    @allure.story("Обновление одного поля")
    @allure.title("Обновление поля price сохраняет остальные поля без изменений")
    @allure.description("Проверяем, что обновление одного поля (price) не затрагивает остальные поля фильма.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_edit_movie_single_field(self, super_admin, create_movie):
        """Позитивный: обновление одного поля (price)"""
        with allure.step("Обновить поле price через PATCH /movies/{id}"):
            new_price = 555
            response = super_admin.api.movies_api.edit_movie(create_movie["id"], {"price": new_price})
            body = response.json()

        with allure.step("Проверить, что price обновился, а остальные поля не изменились"):
            assert body["price"] == new_price
            assert body["name"] == create_movie["name"]
            assert body["location"] == create_movie["location"]

    @allure.story("Обновление нескольких полей")
    @allure.title("Обновление нескольких полей сразу применяется корректно")
    @allure.description("Проверяем, что можно обновить price, description и published одним запросом.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.positive
    @pytest.mark.regression
    def test_edit_movie_multiple_fields(self, super_admin, create_movie):
        """Позитивный: обновление нескольких полей сразу"""
        with allure.step("Обновить price, description и published одним запросом"):
            update_data = {
                "price": 777,
                "description": "Обновлённое описание",
                "published": False
            }
            response = super_admin.api.movies_api.edit_movie(create_movie["id"], update_data)
            body = response.json()

        with allure.step("Проверить, что все переданные поля обновились"):
            assert body["price"] == update_data["price"]
            assert body["description"] == update_data["description"]
            assert body["published"] == update_data["published"]

    @allure.story("Редактирование несуществующего фильма")
    @allure.title("Редактирование несуществующего id возвращает 404")
    @allure.description("Проверяем, что PATCH по заведомо несуществующему id возвращает 404.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_edit_nonexistent_movie(self, super_admin):
        """Негативный: редактирование несуществующего id - 404"""
        with allure.step("Отправить PATCH по несуществующему id - ожидаем 404"):
            nonexistent_id = 999999999
            super_admin.api.movies_api.edit_movie(nonexistent_id, {"price": 100}, expected_status=404)

    @allure.story("Редактирование без авторизации")
    @allure.title("Редактирование фильма анонимным пользователем возвращает 401")
    @allure.description("Проверяем, что без авторизации редактировать фильм нельзя.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_edit_movie_without_auth(self, user_session, create_movie):
        """Негативный: редактирование без авторизации - 401"""
        with allure.step("Попытаться отредактировать фильм без авторизации - ожидаем 401"):
            anonymous = user_session()
            anonymous.movies_api.edit_movie(create_movie["id"], {"price": 100}, expected_status=401)

    @allure.story("Редактирование с невалидным location")
    @allure.title("Редактирование с location вне enum возвращает 400")
    @allure.description("Проверяем валидацию поля location при редактировании фильма.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_edit_movie_invalid_location(self, super_admin, create_movie):
        """Негативный: значение location вне enum - 400"""
        with allure.step("Отправить PATCH с невалидным location - ожидаем 400"):
            super_admin.api.movies_api.edit_movie(
                create_movie["id"], {"location": "NSK"}, expected_status=400
            )
