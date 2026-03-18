import pytest
from models.model_user import RegisterUserResponse, LoginUserResponse

@pytest.mark.order(1)
class TestAuth:

    def test_register_user(self, super_admin, create_user_data):
        """Регистрация пользователя"""
        validation_fields = {"email", "fullName", "roles", "verified"}
        response = super_admin.api.auth_api.register_user(create_user_data.model_dump())
        data_user = RegisterUserResponse.model_validate(response.json())
        actual = data_user.model_dump(include=validation_fields, mode="json")
        expected = create_user_data.model_dump(include=validation_fields)

        assert actual == expected
        assert data_user.id is not None, "Поле id отсутсвует"
        assert data_user.createdAt is not None, "Поле дата регистрации не найдено"

        super_admin.api.user_api.delete_user(data_user.id)#удаление пользователя для освобождения ресурса

    def test_authorization_user(self, super_admin, registered_user, create_user_data):
        """Авторизация зарегестрированого пользователя"""
        validation_fields = {"email", "fullName", "roles"}
        login_data = {
            "email": create_user_data.email,
            "password": create_user_data.password
        }
        response = super_admin.api.auth_api.login_user(login_data)
        data_user = LoginUserResponse.model_validate(response.json())
        actual = data_user.user.model_dump(include=validation_fields, mode="json")
        expected = create_user_data.model_dump(include=validation_fields)
        assert data_user.user.id is not None, "Поле ID ненайдено"
        assert actual == expected
        assert data_user.refreshToken is not None, "Рефреш токен не обнаружен"
        assert data_user.expiresIn is not None, "Данные не обнаружены"
