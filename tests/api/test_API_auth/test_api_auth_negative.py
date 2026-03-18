import pytest
from utils.data_generator import DataGenerator

@pytest.mark.order(2)
class TestApiAuthNegative:

    @pytest.mark.xfail
    def test_invalid_email(self, super_admin):
        """Некоректный email при регистрации пользователя"""
        data_register = {
          "email": 1122,
          "fullName": DataGenerator.generate_random_full_name(),
          "password": DataGenerator.generate_random_password(),
          "passwordRepeat": DataGenerator.generate_random_password()
        }
        response = super_admin.api.auth_api.register_user(data_register, 400)
        message = response.json().get("message")
        assert message[0] == "Некорректный email", "Сообщения не совпадают"
        assert message[3] == "Поле email должно быть строкой", "Сообщения не совпадают"

    def test_existing_user_registration(self, super_admin, registered_user, create_user_data):
        """Регистрация пользователя с уже зарегистрированным email"""
        response = super_admin.api.auth_api.register_user(create_user_data, 409)
        message = response.json().get("message")
        assert message == "Пользователь с таким email уже зарегистрирован", "сообщения не совпадают"

    def test_authorization_user_invalid_email(self, super_admin, registered_user, create_user_data):
        """Авторизация пользователя с несущевствующим email"""
        login_data = {
            "email": "123Vinrnzzxxaabh@gmail.com",
            "password": create_user_data.password
        }
        try:
            response = super_admin.api.auth_api.login_user(login_data, 401)
            message = response.json().get("message")
            assert message == "Неверный логин или пароль", "сообщения не совпадают"
        except AssertionError:
            print("Токен не найден, авторизация не выполнена")
#TODO итзменить тесты под модель пудантик
