import allure
import pytest

from db_models.db_helpers import get_movie_by_id_from_db, get_movie_by_name_from_db


@allure.epic("Cinescope Movies API")
@allure.feature("Синхронизация фильмов с базой данных")
class TestMovieDbSync:
    """Тесты синхронизации данных сервиса с базой данных при создании и удалении фильма."""

    @allure.story("Синхронизация при создании и удалении фильма")
    @allure.title("Фильм появляется в БД после создания через API и пропадает после удаления")
    @allure.description(
        "До создания фильма в БД нет записи с его именем. "
        "После создания через API запись появляется в БД с корректными данными. "
        "После удаления через API запись из БД пропадает."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Artem Sukhovarov")
    @pytest.mark.positive
    @pytest.mark.regression
    @pytest.mark.db
    def test_movie_appears_and_disappears_in_db(self, super_admin, movie_db_sync_data):
        """
        До создания фильма в БД нет записи с его именем.
        После создания через API запись появляется в БД с корректными данными.
        После удаления через API запись из БД пропадает.
        """
        movie_data, genre_id = movie_db_sync_data

        with allure.step("Проверить, что фильма с таким именем ещё нет в БД"):
            assert get_movie_by_name_from_db(movie_data["name"]) is None

        with allure.step("Создать фильм через API"):
            response = super_admin.api.movies_api.create_movie(movie_data)
            created_movie = response.json()
            movie_id = created_movie["id"]

        with allure.step("Проверить, что фильм появился в БД с корректными данными"):
            movie_in_db = get_movie_by_id_from_db(movie_id)
            assert movie_in_db is not None
            assert movie_in_db.name == movie_data["name"]
            assert movie_in_db.price == movie_data["price"]
            assert movie_in_db.genre_id == genre_id

        with allure.step("Удалить фильм через API"):
            super_admin.api.movies_api.delete_movie(movie_id)

        with allure.step("Проверить, что фильм пропал из БД"):
            assert get_movie_by_id_from_db(movie_id) is None
