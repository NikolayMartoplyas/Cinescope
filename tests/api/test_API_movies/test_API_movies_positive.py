from utils.data_generator import DataGenerator
from faker import Faker
faker = Faker("ru_RU")
class TestApiPositive:

    def test_get_list_of_movies(self, auth_manager):
        """Получение афиши фильма"""
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
        response = auth_manager.movies_api.get_movie(payload)
        data_response = response.json()
        assert "movies" in data_response, "Ошибка, отсутсвует ключ movies"
        assert "page" in data_response, "Ошибка, отсутсвует ключ page"
        assert "pageSize" in data_response, "Ошибка, отсутсвует ключ pageSize"

    def test_create_movie(self, auth_manager, movie_data):
        """Создание фильма"""
        response = auth_manager.movies_api.create_movie(movie_data)
        data_response = response.json()
        assert data_response["name"] == movie_data["name"], "Ошибка Названия не совпадают"
        assert data_response["price"] == movie_data["price"], "Ошибка цена не совпадают"
        assert data_response["description"] == movie_data["description"], "Ошибка описание не совпадают"
        id = data_response["id"]
        auth_manager.movies_api.delete_movie(movie_id=id)#Удаляем созданный фильм для очистки рессурса


    def test_get_movie_by_ID(self, auth_manager, create_movie):
        """Получение фильма по ID"""
        response = auth_manager.movies_api.get_movie_by_id(create_movie["id"])
        data_response = response.json()
        assert data_response["name"] == create_movie["create_movie"]["name"], "Ошибка Названия не совпадают"
        assert data_response["price"] == create_movie["create_movie"]["price"], "Ошибка цена не совпадают"
        assert data_response["description"] == create_movie["create_movie"]["description"], "Ошибка описание не совпадают"

    def test_delete_movie_by_ID(self, auth_manager, create_movie):
        """Удаление фильма по ID"""
        auth_manager.movies_api.delete_movie(create_movie["id"])
        response_get = auth_manager.movies_api.get_movie_by_id(create_movie["id"], 404)
        message = response_get.json().get("message")
        assert message == "Фильм не найден", f"Ошибка ожидали сообщение ФИЛЬМ НЕ НАЙДЕН, получили {message}"

    def test_update_movie_title(self, auth_manager, create_movie):
        """Изменение афиши фильма"""
        new_body = DataGenerator.generete_random_movie()
        response = auth_manager.movies_api.update_movie_by_id(create_movie["id"], new_body)
        data_response = response.json()
        assert data_response["name"] == new_body["name"], "Ошибка, название фильмов не совпадают"
        assert data_response["price"] == new_body["price"], "Ошибка, цены не совпадают"
        assert data_response["description"] == new_body["description"], "Ошибка, описание фильмов не совпадают"
        assert data_response["published"] == new_body["published"], "Ошибка, публикации фильмов не совпадают"
        assert data_response["genreId"] == new_body["genreId"], "Ошибка, название жанр не совпадают"