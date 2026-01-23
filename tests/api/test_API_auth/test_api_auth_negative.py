import pytest
from utils.data_generator import DataGenerator

@pytest.mark.order(2)
class TestApiAuthNegative:

    def test_invalid_email(self, api_manager):
        """Некоректный email при регистрации пользователя"""
        data_register = {
          "email": 1122,
          "fullName": DataGenerator.generate_random_full_name(),
          "password": DataGenerator.generate_random_password(),
          "passwordRepeat": DataGenerator.generate_random_password()
        }
        response = api_manager.auth_api.register_user(data_register, 400)
        message = response.json().get("message")
        assert message[0] == "Некорректный email", "Сообщения не совпадают"
        assert message[3] == "Поле email должно быть строкой", "Сообщения не совпадают"

    def test_existing_user_registration(self, api_manager, registered_user, create_user):
        """Регистрация пользователя с уже зарегистрированным email"""
        response = api_manager.auth_api.register_user(create_user, 409)
        message = response.json().get("message")
        assert message == "Пользователь с таким email уже зарегистрирован", "сообщения не совпадают"

    def test_authorization_with_an_invalid_email(self,api_manager, create_user):
        """Авторизация пользователя с несущевствующим email"""
        login_data = {
            "email": "123Vinrnzzxxaabh@gmail.com",
            "password": create_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data, 401)
        message = response.json().get("message")
        assert message == "Неверный логин или пароль", "сообщения не совпадают"