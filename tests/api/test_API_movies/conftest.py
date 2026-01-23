from faker import Faker
import pytest
import requests

from api.api_manager import ManagerApi
from constants import *
from custom_requester.custom_requester import CustomRequester

faker = Faker("ru_RU")
@pytest.fixture(scope="session")
def base_session():
    """Базовая сессия"""
    session = requests.Session()
    yield session
    session.close()

@pytest.fixture(scope="session")
def anon_manager():
    """менеджер для неавторизованных запросов"""
    session = requests.Session()
    session.headers.update(HEADERS)
    return ManagerApi(session)

@pytest.fixture(scope="session")
def auth_manager(base_session):
    """менеджер для авторизованых запросов"""
    api_manager = ManagerApi(base_session)
    response = api_manager.auth_api.login_user(AUTH_DATE, 200)
    token = response.json().get("accessToken")
    assert token is not None, "Ошибка токен не найден"
    custom_requester = CustomRequester(base_session, MOVIE_URL)
    custom_requester._update_session_headers(Authorization=f"Bearer {token}")
    return api_manager

@pytest.fixture()
def create_movie(auth_manager, movie_data):
    """Создание афиши фильма и удаление фильма после выполнения теста"""
    response = auth_manager.movies_api.creating_movie_poster(movie_data, 201)
    data_response = response.json()
    id = data_response["id"]
    yield {"id": id, "create_movie": data_response}
    requests.delete(f"{MOVIE_URL}{ENDPOINT_MOVIES}/{id}")#Выполняем удаление без сессии чтоб небыло ошибки если фильм удалится в тесте

@pytest.fixture()
def movie_data():
    """Генератор афиши фильма"""
    return {
        "name": f"{faker.company()} - {faker.catch_phrase()}",
        "imageUrl": "https://image.url",
        "price": faker.random_int(100, 1000),
        "description": faker.text(max_nb_chars=100),
        "location": "SPB",
        "published": faker.boolean(),
        "genreId": faker.random_int(1, 10)
    }