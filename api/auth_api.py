from custom_requester.custom_requester import CustomRequester
from constants import AUTH_URL, ENDPOINT_REGISTER, ENDPOINT_LOGIN

class AuthApi(CustomRequester):
    """Класс для работы с аутентификацией"""

    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_URL)

    def register_user(self, data, expected_status=201):
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код
        """
        return self.send_request(
            method="POST",
            endpoint=ENDPOINT_REGISTER,
            data=data,
            expected_status=expected_status
        )

    def login_user(self, data, expected_status=200):
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        response = self.send_request(
            method="POST",
            endpoint=ENDPOINT_LOGIN,
            data=data,
            expected_status=expected_status
        )
        token = response.json().get("accessToken")
        assert token is not None, "Токен не найден"
        self._update_session_headers(Authorization=f"Bearer {token}")
        return response

