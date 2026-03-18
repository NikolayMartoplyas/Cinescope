import pytest
from models.model_user import RegisterUserResponse

@pytest.fixture(scope="module")
def registered_user(super_admin, create_user_data):
    """Регистрация пользователя"""
    response = super_admin.api.auth_api.register_user(create_user_data)
    data_user = RegisterUserResponse.model_validate(response.json())
    yield data_user
    id = getattr(data_user, "id", None)
    if id:
        del_res = super_admin.api.user_api.delete_user(id)
        if del_res.status_code not in (200, 201):
            print("пользователь удален в тесте")
        else:
            print("Пользовател удален в фикстуре")
