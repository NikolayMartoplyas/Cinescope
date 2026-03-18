import random
import allure
import pytest
from tests.conftest import admin, super_admin, common_user
from utils.data_generator import DataGenerator
from faker import Faker
from models.model_movies import MoviesModelResponse, MoviesModelErrorResponse

faker = Faker("ru_RU")

@allure.epic("Тестирование афиш фильма")
@allure.feature("""Получение списка фильмов, параметризированный тест, создание
получение фильма оп ID, удаление фильма, Изменение афиши фильма, создание фильма с ролью USER
""")
class TestApiPositive:

    @allure.story("Получение афиши фильма")
    @pytest.mark.slow
    @pytest.mark.movie
    def test_get_list_of_movies(self, super_admin):
        with allure.step("Подотавка payload"):
            payload = {
                'pageSize': 1,
                'page': 1,
                'minPrice': 1,
                'maxPrice': 1000,
                'locations': ['MSK', 'SPB'],
                'published': 'true',
                'genreId': 1,
                'createdAt': 'asc'
            }
        with allure.step("Отправка заппрос и Десериализация ответа"):
            response = super_admin.api.movies_api.get_movie(payload)
            data_response = response.json()
        with allure.step("Assert"):
            assert "movies" in data_response, "Ошибка, отсутсвует ключ movies"
            assert "page" in data_response, "Ошибка, отсутсвует ключ page"
            assert "pageSize" in data_response, "Ошибка, отсутсвует ключ pageSize"

    @allure.story("Параметризированный тест, на получение афиш фильма")
    @allure.description("""
    Шаги:
    1. Подотавка payload
    2. Отправка заппрос и Десериализация ответа
    3. Assert 
    """)
    @pytest.mark.slow
    @pytest.mark.movie
    @pytest.mark.parametrize("minPrice,maxPrice,locations,genreID",
                             [(1, 1000, "MSK", random.randint(1, 10)),
                              (1, 1000, "SPB", random.randint(1, 10))],
                             ids= ["locations MSK", "locations SPB"])
    def test_get_list_movie_different_parameters(self, minPrice, maxPrice, locations , genreID, common_user):
        with allure.step("Подотавка payload"):
            payload = {
                'pageSize': 1,
                'page': 1,
                'minPrice': minPrice,
                'maxPrice': maxPrice,
                'locations': locations,
                'published': 'true',
                'genreId': genreID,
                'createdAt': 'asc'
            }

        with allure.step("Отправка заппрос и Десериализация ответа"):
            response = common_user.api.movies_api.get_movie(payload)
            data_response = response.json()

        with allure.step("Assert"):
            assert "movies" in data_response, "Ошибка, отсутсвует ключ movies"
            assert "page" in data_response, "Ошибка, отсутсвует ключ page"
            assert "pageSize" in data_response, "Ошибка, отсутсвует ключ pageSize"

    @allure.story("Создание фильма")
    @pytest.mark.movie
    def test_create_movie(self, super_admin, movie_data, validation_fields):
        with allure.step("Создание фильма"):
            response = super_admin.api.movies_api.create_movie(movie_data)

        with allure.step("Проверка ответа моделью пудантик"):
            validate_response = MoviesModelResponse.model_validate(response.json())

        with allure.step("подготовка ожидаемого и фактического результата и их сравнение"):
            actual_movies = validate_response.model_dump(include=validation_fields, mode="json")
            expected_movies = movie_data.model_dump(include=validation_fields)
            assert actual_movies == expected_movies, "Поля не совпадают"

        with allure.step("Удаление фильма для освобождения ресурса"):
            super_admin.api.movies_api.delete_movie(movie_id=validate_response.id)#Удаляем созданный фильм для очистки рессурса

    @allure.story("Получение фильма по ID")
    @pytest.mark.movie
    def test_get_movie_by_ID(self, super_admin, create_movie, validation_fields):
        with allure.step("Получение фильма по ID"):
            response = super_admin.api.movies_api.get_movie_by_id(create_movie.id)

        with allure.step("Проверка ответа моделью пудантик"):
            validate_response = MoviesModelResponse.model_validate(response.json())

        with allure.step("подготовка ожидаемого и фактического результата и их сравнение"):
            actual_movies = validate_response.model_dump(include=validation_fields, mode="json")
            expected_movies = create_movie.model_dump(include=validation_fields)
            assert actual_movies == expected_movies, "Поля не совпадают"

    @allure.story("Удаление фильма по ID")
    @pytest.mark.movie
    def test_delete_movie_by_ID(self, super_admin, create_movie):
        with allure.step("Получение фильма по ID"):
            super_admin.api.movies_api.delete_movie(create_movie.id)

        with allure.step("Отправка GET запроса для проверки удаления пользователя"):
            response_get = super_admin.api.movies_api.get_movie_by_id(create_movie.id, 404)

        with allure.step("Валидация ответа через модель пудантик"):
            validate_response = MoviesModelErrorResponse.model_validate(response_get.json())

        with allure.step("Assert"):
            assert validate_response.error == "Not Found", "Название ошибки не совпадает"
            assert validate_response.message == "Фильм не найден", "Ожидали что фильм неайден не будет"

    @allure.story("Изменение афиши фильма")
    @pytest.mark.movie
    def test_update_movie_title(self, super_admin, create_movie, validation_fields):
        with allure.step("Подготовка нового фильма и отправка запроса на обновления сущевствующенго фильма"):
            new_body = DataGenerator.generete_random_movie()
            response = super_admin.api.movies_api.update_movie_by_id(create_movie.id, new_body)

        with allure.step("Валидация ответа через модель пудантик"):
            validate_response = MoviesModelResponse.model_validate(response.json())

        with allure.step("подготовка ожидаемого и фактического результата и их сравнение"):
            actual_movies = validate_response.model_dump(include=validation_fields, mode="json")
            expected_movies = new_body.model_dump(include=validation_fields)
            assert actual_movies == expected_movies, "Поля не совпадают"

    @allure.story("Создание фильма с ролью USER")
    @pytest.mark.movie
    def test_create_movie_roles_of_user(self, common_user, movie_data):
        with allure.step("Создание фильма"):
            response = common_user.api.movies_api.create_movie(movie_data, 403)

        with allure.step("Валидация ответа через модель пудантик"):
            validate_response = MoviesModelErrorResponse.model_validate(response.json())

        with allure.step("Assert"):
            assert validate_response.error == "Forbidden", "Название ошибки не совпадает"
            assert validate_response.message == "Forbidden resource", "Ожидали что фильм неайден не будет"


    @pytest.mark.movie
    @pytest.mark.skip(reason="Временно отключен")
    def test_create_movie_roles_of_admin(self, admin, movie_data):
        """Создание фильма с ролью ADMIN"""
        response = admin.api.movies_api.create_movie(movie_data, expected_status=403)
        message = response.json().get("message")
        assert message == "Forbidden resource", "Сообщения не совпадают"



