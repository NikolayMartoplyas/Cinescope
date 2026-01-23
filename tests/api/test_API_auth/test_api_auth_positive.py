import pytest
from api.api_manager import ManagerApi

@pytest.mark.order(1)
class TestAuth:

    def test_register_user(self, api_manager: ManagerApi, create_user):
        """Регистрация пользователя"""
        response = api_manager.auth_api.register_user(create_user, 201)
        response_data = response.json()
        assert "id" in response_data, "Поле id отсутсвует"
        assert response_data["email"] == create_user["email"], "Еmail не совпадает"
        assert response_data["fullName"] == create_user["fullName"], "Имя не совпадает"
        assert "verified" in response_data, "Поле не найдено"
        assert response_data["roles"][0] == "USER", "Роль не совпадает"
        assert "createdAt" in response_data, "Поле дата регистрации не найдено"

    def test_authorization_user(self, api_manager, registered_user, create_user):
        """Авторизация зарегестрированого пользователя"""
        login_data = {
            "email": create_user["email"],
            "password": create_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data, 200)
        authorization_data = response.json()
        assert "id" in authorization_data["user"], "Поле ID ненайдено"
        assert "email" in authorization_data["user"], "Поле email ненайдено"
        assert "fullName" in authorization_data["user"], "Поле fullName ненайдено"
        assert "roles" in authorization_data["user"], "Поле roles ненайдено"
        assert "accessToken" is not None, "Токен не обнаружен"
        assert "refreshToken" is not None, "Рефреш токен не обнаружен"
        assert "expiresIn" is not None, "Данные не обнаружены"
