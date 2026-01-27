from faker import Faker
import pytest
import requests

from api.api_manager import ManagerApi
from constants import *
from utils.data_generator import DataGenerator

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
    api_manager.auth_api.login_user(AUTH_DATE, 200)
    return api_manager

@pytest.fixture()
def create_movie(auth_manager, movie_data):
    """Создание афиши фильма и удаление фильма после выполнения теста"""
    response = auth_manager.movies_api.create_movie(movie_data)
    data_response = response.json()
    id = data_response["id"]
    yield {"id": id, "create_movie": data_response}
    try:
        auth_manager.movies_api.get_movie_by_id(id)
    except Exception as e:
        print("Фильм удален в тесте")

@pytest.fixture()
def movie_data():
    """Генератор афиши фильма"""
    return DataGenerator.generete_random_movie()