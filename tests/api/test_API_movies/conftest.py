from faker import Faker
import pytest
import requests
from api.api_manager import ManagerApi
from constants import *
from utils.data_generator import DataGenerator
from models.model_movies import MoviesModelResponse

faker = Faker("ru_RU")
@pytest.fixture(scope="session")
def anon_manager():
    """менеджер для неавторизованных запросов"""
    session = requests.Session()
    session.headers.update(HEADERS)
    return ManagerApi(session)

@pytest.fixture()
def create_movie(super_admin, movie_data):
    """Создание афиши фильма и удаление фильма после выполнения теста"""
    response = super_admin.api.movies_api.create_movie(movie_data.model_dump())
    validate_movies = MoviesModelResponse.model_validate(response.json())
    yield validate_movies
    try:
        get_response = super_admin.api.movies_api.get_movie_by_id(validate_movies.id)
        if get_response.status_code in (201, 200):
            super_admin.api.movies_api.delete_movie(validate_movies.id)
            print("Фильм удален в фикстуре")
    except Exception as e:
        print("Фильм удален в тесте")

@pytest.fixture()
def movie_data():
    """Генератор афиши фильма"""
    return DataGenerator.generete_random_movie()

@pytest.fixture()
def movie_data_in_db():
    """Генератор афиши фильма для БД"""
    return DataGenerator.generete_random_movie_in_db()

@pytest.fixture()
def validation_fields():
    return {"name", "imageUrl", "price", "description", "location", "published", "genreId"}


