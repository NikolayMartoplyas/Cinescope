import requests
import pytest
from api.api_manager import ManagerApi
from  entities.user import User
from models.model_user import UserTest
from resources.user_creds import SuperAdminCreds
from constant.roles import Roles
from utils.data_generator import DataGenerator
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_manager import DBHelper
from models.model_user import RegisterUserResponse

@pytest.fixture(scope="module")
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ManagerApi(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture(scope="module")
def create_user_data(create_user):
    update_user = create_user.model_copy(update={
        "verified": True,
        "banned": False
    })
    return update_user

@pytest.fixture(scope="module")
def create_user() -> UserTest:
    random_email = DataGenerator.generate_random_email()
    random_full_name = DataGenerator.generate_random_full_name()
    random_password = DataGenerator.generate_random_password()

    return UserTest(
        email=random_email,
        fullName=random_full_name,
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture(scope="module")
def common_user(user_session, create_user_data, super_admin):
    """Создание обычного пользователя"""
    new_session = user_session()
    common_user = User(
        create_user_data.email,
        create_user_data.password,
        [Roles.USER.value],
        new_session
    )
    response = super_admin.api.user_api.create_user(create_user_data.model_dump())
    validate_rsponse = RegisterUserResponse.model_validate(response.json())
    common_user.api.auth_api.login_user(common_user.creds)
    yield common_user
    try:
        response_get = super_admin.api.user_api.get_user_info_by_locator(validate_rsponse.id)
        if response_get.status_code in (200, 201):
            super_admin.api.user_api.delete_user(validate_rsponse.id)
    except ValueError as e:
        print(f"Пользователь USER удален в тесте, {e}")

@pytest.fixture(scope="module")
def admin(user_session, create_user_data, super_admin):
    new_session = user_session()
    admin = User(
        create_user_data.email,
        create_user_data.password,
        [Roles.ADMIN.value],
        new_session
    )
    response = super_admin.api.user_api.create_user(create_user_data)
    validate_response = RegisterUserResponse.model_validate(response.json())
    admin.api.auth_api.login_user(admin.creds)
    yield admin
    try:
        response_get = super_admin.api.user_api.get_user_info_by_id(validate_response.id)
        if response_get.status_code in (200, 201):
            super_admin.api.user_api.delete_user(validate_response.id)
    except ValueError as e:
        print(f"Пользователь ADMIN удален в тесте, {e}")

@pytest.fixture(scope="module")
def super_admin(user_session):
    """Создание супер админа"""
    new_session = user_session()
    super_admin = User(SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD, [Roles.SUPER_ADMIN.value], new_session)
    super_admin.api.auth_api.login_user(super_admin.creds)
    return super_admin

@pytest.fixture(scope="module")
def db_session() -> Session:
    """Фикстура которая создает подключение к БД
    а после звершения теста закрывает соединение"""
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """Фикстура для передачи хелпера в тесты для работы с БД"""
    db_helper = DBHelper(db_session)
    return db_helper