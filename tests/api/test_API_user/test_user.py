import requests

from api.api_manager import ManagerApi
from constants import AUTH_PASSWORD, AUTH_EMAIL, AUTH_DATE
from entities.user import User


class TestUser:

    def test_1(self, super_admin):
        print(f"Session headers: {super_admin.api.auth_api.headers}")