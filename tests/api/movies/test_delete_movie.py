import allure
import pytest

from utils.data_generator import DataGenerator


@allure.epic("Cinescope Movies API")
@allure.feature("Удаление фильма (DELETE /movies/{id})")
class TestDeleteMovie:
    """Тесты для DELETE - удаление фильма"""

    @allure.story("Успешное удаление фильма")
    @allure.title("Удаление существующего фильма делает его недоступным по id")
    @allure.description("Проверяем, что после удаления фильм пропадает и запрос по его id возвращает 404.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_delete_movie_success(self, super_admin):
        """Позитивный: удаление существующего фильма"""
        with allure.step("Создать фильм для удаления"):
            genre_id = super_admin.api.movies_api.get_genres()[0]["id"]
            movie_data = DataGenerator.generate_movie_data(genre_id)
            created_movie = super_admin.api.movies_api.create_movie(movie_data).json()

        with allure.step("Удалить фильм через DELETE /movies/{id}"):
            response = super_admin.api.movies_api.delete_movie(created_movie["id"])
            assert response.json()["id"] == created_movie["id"]

        with allure.step("Проверить, что фильм больше не доступен по id - ожидаем 404"):
            super_admin.api.movies_api.get_movie_by_id(created_movie["id"], expected_status=404)

    @allure.story("Повторное удаление фильма")
    @allure.title("Повторное удаление уже удалённого фильма возвращает 404")
    @allure.description("Проверяем, что второе удаление того же фильма возвращает 404.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_delete_movie_twice(self, super_admin):
        """Негативный: повторное удаление уже удалённого фильма - 404"""
        with allure.step("Создать и удалить фильм"):
            genre_id = super_admin.api.movies_api.get_genres()[0]["id"]
            movie_data = DataGenerator.generate_movie_data(genre_id)
            created_movie = super_admin.api.movies_api.create_movie(movie_data).json()
            super_admin.api.movies_api.delete_movie(created_movie["id"])

        with allure.step("Повторно удалить тот же фильм - ожидаем 404"):
            super_admin.api.movies_api.delete_movie(created_movie["id"], expected_status=404)

    @allure.story("Удаление несуществующего фильма")
    @allure.title("Удаление заведомо несуществующего id возвращает 404")
    @allure.description("Проверяем, что DELETE по несуществующему id возвращает 404.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_delete_nonexistent_movie(self, super_admin):
        """Негативный: удаление заведомо несуществующего id - 404"""
        with allure.step("Отправить DELETE по несуществующему id - ожидаем 404"):
            nonexistent_id = 999999999
            super_admin.api.movies_api.delete_movie(nonexistent_id, expected_status=404)

    @allure.story("Удаление без авторизации")
    @allure.title("Удаление фильма анонимным пользователем возвращает 401")
    @allure.description("Проверяем, что без авторизации удалить фильм нельзя.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_delete_movie_without_auth(self, user_session, create_movie):
        """Негативный: удаление без авторизации - 401"""
        with allure.step("Попытаться удалить фильм без авторизации - ожидаем 401"):
            anonymous = user_session()
            anonymous.movies_api.delete_movie(create_movie["id"], expected_status=401)
