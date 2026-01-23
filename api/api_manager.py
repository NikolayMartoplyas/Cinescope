from .auth_api import AuthApi
from .user_api import UserApi
from .movies_api import MoviesApi

class ManagerApi:
    """Класс для централизованного управления классами API в одной сессии"""

    def __init__(self, session):
        self.session = session
        self.auth_api = AuthApi(session)
        self.user_api = UserApi(session)
        self.movies_api = MoviesApi(session)

