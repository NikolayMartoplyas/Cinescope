from constants import ENDPOINT_MOVIES
from faker import Faker
faker = Faker("ru_RU")
class TestApiPositive:

    def test_getting_list_of_movies(self, auth_manager):
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
        response = auth_manager.movies_api.get_poster_movie(payload, 200)
        date_response = response.json()
        assert "movies" in date_response, "Ошибка, отсутсвует ключ movies"
        assert "page" in date_response, "Ошибка, отсутсвует ключ page"
        assert "pageSize" in date_response, "Ошибка, отсутсвует ключ pageSize"

    def test_creating_a_movie_poster(self, auth_manager, movie_data):
        """Создание афиши фильма"""
        response = auth_manager.movies_api.creating_movie_poster(movie_data, 201)
        date_response = response.json()
        assert date_response["name"] == movie_data["name"], "Ошибка Названия не совпадают"
        assert date_response["price"] == movie_data["price"], "Ошибка цена не совпадают"
        assert date_response["description"] == movie_data["description"], "Ошибка описание не совпадают"
        id = date_response["id"]
        auth_manager.movies_api.delete_movie(movie_id=id, expected_status=200)#Удаляем созданный фильм для очистки рессурса


    def test_getting_movie_by_ID(self, auth_manager, create_movie, movie_data):
        """Получение фильма по ID"""
        response = auth_manager.movies_api.get_movie_by_id(create_movie["id"], 200)
        date_response = response.json()
        assert date_response["name"] == movie_data["name"], "Ошибка Названия не совпадают"
        assert date_response["price"] == movie_data["price"], "Ошибка цена не совпадают"
        assert date_response["description"] == movie_data["description"], "Ошибка описание не совпадают"

    def test_delete_movie_by_ID(self, auth_manager, create_movie):
        """Удаление фильма по ID"""
        auth_manager.movies_api.delete_movie(create_movie["id"], 200)
        response_get = auth_manager.movies_api.get_movie_by_id(create_movie["id"], 404)
        message = response_get.json().get("message")
        assert message == "Фильм не найден", f"Ошибка ожидали сообщение ФИЛЬМ НЕ НАЙДЕН, получили {message}"

    def test_changing_the_title_of_the_movie_by_id(self, auth_manager, create_movie):
        """Изменение афиши фильма"""
        new_body = {
            "name": f"{faker.company()} - {faker.catch_phrase()}",
            "imageUrl": "https://image.url",
            "price": faker.random_int(100, 1000),
            "description": faker.text(max_nb_chars=100),
            "location": "SPB",
            "published": faker.boolean(),
            "genreId": faker.random_int(1, 10)
        }
        response = auth_manager.movies_api.editing_a_movie_by_id(create_movie["id"], new_body, 200)
        data_response = response.json()
        assert data_response["name"] == new_body["name"], "Ошибка, название фильмов не совпадают"
        assert data_response["price"] == new_body["price"], "Ошибка, название фильмов не совпадают"
        assert data_response["description"] == new_body["description"], "Ошибка, название фильмов не совпадают"
        assert data_response["published"] == new_body["published"], "Ошибка, название фильмов не совпадают"
        assert data_response["genreId"] == new_body["genreId"], "Ошибка, название фильмов не совпадают"