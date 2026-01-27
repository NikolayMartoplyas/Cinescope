import requests
import pytest
from api.api_manager import ManagerApi
from  entities.user import User
from constants import AUTH_EMAIL, AUTH_PASSWORD
from ..test_API_auth.conftest import create_user


@pytest.fixture(scope="session")
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ManagerApi(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session()

    for user in user_pool:
        user.close_session()

@pytest.fixture(scope="session")
def super_admin(user_session):
    new_session = user_session
    super_admin = User(AUTH_EMAIL, AUTH_PASSWORD, ["SUPER_ADMIN"], new_session)
    super_admin.api.auth_api.login_user(super_admin.creds, 200)
    return super_admin

@pytest.fixture(scope="session")
def create_user_data(create_user):
    update_data = create_user.copy()
    update_data.update({
        "verified": True,
        "banned": False
    })
    return update_data
