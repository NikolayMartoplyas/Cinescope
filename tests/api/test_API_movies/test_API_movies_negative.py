import pytest
from faker import Faker
from models.model_movies import MoviesModelErrorResponse

faker = Faker()

class TestApiMoviesNegative:

    @pytest.mark.slow
    @pytest.mark.movie
    def test_invalid_data_type_in_parameters(self, super_admin):
        """Невалидный тип данных"""
        payload = {
            'pageSize': "вав",
            'page': 1,
            'minPrice': 1,
            'maxPrice': 1000,
            'locations': ['MSK', 'SPB'],
            'published': 'true',
            'genreId': 1,
            'createdAt': 'asc'
        }
        text_error = [
            "Поле pageSize имеет максимальную величину 20",
            "Поле pageSize имеет минимальную величину 1",
            "Поле pageSize должно быть целым числом"
        ]
        response = super_admin.api.movies_api.get_movie(payload, 400)
        validate_response = MoviesModelErrorResponse.model_validate(response.json())
        assert validate_response.error == "Bad Request", "Сообщения не совпадают"
        for text in text_error:
            assert text in validate_response.message


    @pytest.mark.movie
    def test_create_movie_with_incorrect_parameters(self, super_admin):
        """Создание фильма с некорректными параметрами"""
        request_body = {
            "name": 22,
            "imageUrl": "https://image.url",
            "price": faker.random_int(100, 1000),
            "description": faker.text(max_nb_chars=100),
            "location": "SPB",
            "published": faker.boolean(),
            "genreId": 1
        }
        text_error = [
            "Поле name должно содержать не менее 3 символов",
            "Поле name должно быть строкой"
        ]
        response = super_admin.api.movies_api.create_movie(request_body, 400)
        validate_response = MoviesModelErrorResponse.model_validate(response.json())
        assert validate_response.error == "Bad Request", "Ошибки не совпадают"
        for text in text_error:
            assert text in validate_response.message

    @pytest.mark.slow
    @pytest.mark.movie
    def test_creation_movie_unauthorized_user(self,anon_manager, movie_data):
        """Создание фильма с неавторизованым пользователем"""
        response = anon_manager.movies_api.create_movie(movie_data, 401)
        validate_response = MoviesModelErrorResponse.model_validate(response.json())
        assert validate_response.message == "Unauthorized", f"Ошибка ожидали сообщение Unauthorized, получили {validate_response.message}"

    @pytest.mark.movie
    def test_deleting_movie_unauthorized_user(self,anon_manager, create_movie):
        """Удаление фильма неавторизованым пользователем"""
        response = anon_manager.movies_api.delete_movie(create_movie.id, 401)
        validate_response = MoviesModelErrorResponse.model_validate(response.json())
        assert validate_response.message == "Unauthorized", f"Ошибка ожидали сообщение Unauthorized, получили {validate_response.message}"

    @pytest.mark.movie
    def test_update_movie_unauthorized_user(self, anon_manager, create_movie, movie_data):
        """Редактирование фильма неавторизованым пользователем"""
        new_response_body = movie_data
        response = anon_manager.movies_api.update_movie_by_id(create_movie.id, new_response_body, 401)
        validate_response = MoviesModelErrorResponse.model_validate(response.json())
        assert validate_response.message == "Unauthorized", f"Ошибка ожидали сообщение Unauthorized, получили {validate_response.message}"

    @pytest.mark.movie
    def test_create_film_existing_title(self, super_admin, create_movie, movie_data):
        """Создание фильма с уже существующим названием"""
        response = super_admin.api.movies_api.create_movie(movie_data, 409)
        validate_response = MoviesModelErrorResponse.model_validate(response.json())
        assert validate_response.message == "Фильм с таким названием уже существует", "Ошибка сообщения не совпадают"
        assert validate_response.error == "Conflict", "Название ошибки не совпадает"


