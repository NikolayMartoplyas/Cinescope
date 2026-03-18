import allure
from faker import Faker

faker = Faker()

@allure.epic("Тестирование фильма в БД")
@allure.feature("Фильм корректно добавляется в БД")
class TestMovieDB:

    @allure.story("Создание фильма в БД и Удаление")
    def test_create_movie_in_db(self, db_helper, movie_data_in_db, super_admin):
        with allure.step("Добавление фильма в БД"):
            create_movie = db_helper.movie.create_movie_in_db(movie_data_in_db)
            assert create_movie is not None, "Фильм не найден"

        with allure.step("Получение филма из БД по ID"):
            get_movie = db_helper.movie.get_movie_by_id(create_movie.id)
            assert create_movie == get_movie

        with allure.step("Удаление фильма в БД"):
            super_admin.api.movies_api.delete_movie(create_movie.id)
            get_movie = db_helper.movie.get_movie_by_id(create_movie.id)
            assert get_movie is None, "Фильм не удалился"

