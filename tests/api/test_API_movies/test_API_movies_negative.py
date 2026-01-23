import requests
from faker import Faker

faker = Faker()
class TestApiMoviesNegative:

    def test_invalid_data_type_in_parameters(self, auth_manager):
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
        response = auth_manager.movies_api.get_poster_movie(payload, 400)
        message = response.json().get("message")
        assert message[0] == "Поле pageSize имеет максимальную величину 20", "Сообщения не совпадают"
        assert message[1] == "Поле pageSize имеет минимальную величину 1", "Сообщения не совпадают"
        assert message[2] == "Поле pageSize должно быть числом", "Сообщения не совпадают"

    def test_creating_a_movie_poster_with_incorrect_parameters(self, auth_manager):
        """Создание постера с некорректными параметрами"""
        request_body = {
            "name": 22,
            "imageUrl": "https://image.url",
            "price": faker.random_int(100, 1000),
            "description": faker.text(max_nb_chars=100),
            "location": "SPB",
            "published": faker.boolean(),
            "genreId": 1
        }
        response = auth_manager.movies_api.creating_movie_poster(request_body, 400)
        message = response.json().get("message")
        assert message[0] == "Поле name должно быть строкой", "Сообщения не совпадают"

    def test_creation_of_a_poster_by_an_unauthorized_user(self,anon_manager, movie_data):
        """Создание постера с неавторизованым пользователем"""
        response = anon_manager.movies_api.creating_movie_poster(movie_data, 401)
        message = response.json().get("message")
        assert message == "Unauthorized", f"Ошибка ожидали сообщение Unauthorized, получили {message}"

    def test_deleting_a_user_with_an_unauthorized_user(self,anon_manager, create_movie):
        """Удаление фильма неавторизованым пользователем"""
        response = anon_manager.movies_api.delete_movie(create_movie["id"], 401)
        data_response = response.json().get("message")
        assert data_response == "Unauthorized", f"Ошибка ожидали сообщение Unauthorized, олучили {data_response}"

    def test_editing_a_movie_by_an_unauthorized_user(self,anon_manager, create_movie, movie_data):
        """Редактирование фильма неавторизованым пользователем"""
        new_response_body = movie_data
        response = anon_manager.movies_api.editing_a_movie_by_id(create_movie["id"], new_response_body, 401)
        data_response = response.json().get("message")
        assert data_response == "Unauthorized", f"Ошибка ожидали сообщение Unauthorized, олучили {data_response}"