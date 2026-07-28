import allure
import pytest

from utils.data_generator import DataGenerator


@allure.epic("Cinescope Movies API")
@allure.feature("Права доступа к фильмам по ролям")
class TestMoviesAccess:
    """Тесты прав доступа для разных ролей."""

    @allure.story("USER не может создавать фильмы")
    @allure.title("Пользователь с ролью USER получает 403 при создании фильма")
    @allure.description("Проверяем, что создавать фильмы может только SUPER_ADMIN.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.negative
    @pytest.mark.regression
    @pytest.mark.roles
    def test_common_user_cannot_create_movie(self, super_admin, common_user):
        """Негативный: пользователь с ролью USER не может создать фильм - 403"""
        with allure.step("Сгенерировать данные фильма"):
            genre_id = super_admin.api.movies_api.get_genres()[0]["id"]
            movie_data = DataGenerator.generate_movie_data(genre_id)

        with allure.step("Попытаться создать фильм от лица USER - ожидаем 403"):
            common_user.api.movies_api.create_movie(movie_data, expected_status=403)

    @allure.story("Фикстура admin рабочая")
    @allure.title("Фикстура admin создаёт рабочего пользователя с ролью ADMIN")
    @allure.description("Проверяем, что фикстура admin выдаёт авторизованного пользователя, способного делать запросы.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.positive
    @pytest.mark.regression
    @pytest.mark.roles
    def test_admin_fixture_works(self, admin):
        """Проверка, что фикстура admin создаёт рабочего юзера с ролью ADMIN"""
        with allure.step("Выполнить запрос GET /movies от лица admin"):
            response = admin.api.movies_api.get_movies(params={"pageSize": 2})

        with allure.step("Проверить, что запрос прошёл успешно (200)"):
            assert response.status_code == 200

    @allure.story("Удаление фильма по ролям")
    @allure.title("Удаление фильма ролью {user_fixture_name} -> ожидаем {expected_status}")
    @allure.description(
        "Проверяем права на удаление фильма для разных ролей: "
        "удалять фильм может только SUPER_ADMIN, USER и ADMIN получают 403."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.parametrize(
        "user_fixture_name, expected_status",
        [
            pytest.param("common_user", 403, marks=pytest.mark.negative),
            pytest.param("admin", 403, marks=pytest.mark.negative),
            pytest.param("super_admin", 200, marks=pytest.mark.positive),
        ],
        ids=["USER запрещено", "ADMIN запрещено", "SUPER_ADMIN разрешено"]
    )
    @pytest.mark.regression
    @pytest.mark.roles
    def test_delete_movie_by_role(self, request, create_movie, user_fixture_name, expected_status):
        """Проверка прав на удаление фильма (по документации может удалять только SUPER_ADMIN"""
        with allure.step(f"Получить фикстуру пользователя {user_fixture_name}"):
            user = request.getfixturevalue(user_fixture_name)

        with allure.step(f"Удалить фильм от лица {user_fixture_name} - ожидаем {expected_status}"):
            user.api.movies_api.delete_movie(create_movie["id"], expected_status=expected_status)
