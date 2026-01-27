from api.api_manager import ManagerApi

class User:

    def __init__(self, email: str, password: str, roles: list, api: ManagerApi):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api

    @property
    def creds(self):
        """Возврашаем креды пользователя"""
        return {
          "email": self.email,
          "password": self.password
        }
