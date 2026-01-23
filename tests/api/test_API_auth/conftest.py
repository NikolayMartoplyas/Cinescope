import pytest
import requests
from utils.data_generator import DataGenerator
from api.api_manager import ManagerApi

@pytest.fixture(scope="session")
def session():
    """Создание сессии"""
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """Фикстура для создания экземпляра ApiManager."""
    return ManagerApi(session)

@pytest.fixture()
def create_user():
    random_email = DataGenerator.generate_random_email()
    random_full_name = DataGenerator.generate_random_full_name()
    random_password = DataGenerator.generate_random_password()

    return {
      "email": random_email,
      "fullName": random_full_name,
      "password": random_password,
      "passwordRepeat": random_password
    }

@pytest.fixture()
def registered_user(api_manager, create_user):
    """Регистрация пользователя"""
    response = api_manager.auth_api.register_user(create_user, 201)
    response_data = response.json()
    return response_data



