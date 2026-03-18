import pytest
from models.model_user import RegisterUserResponse

@pytest.fixture()
def user(create_user_data, super_admin):
    response = super_admin.api.user_api.create_user(create_user_data.model_dump())
    validate_response = RegisterUserResponse.model_validate(response.json())
    yield validate_response
    try:
        response_get = super_admin.api.user_api.get_user_info_by_locator(validate_response.id)
        if response_get.status_code in (200, 201):
            super_admin.api.user_api.delete_user(validate_response.id)
    except ValueError as e:
        print(f"Пользователь удален в тесте, {e}")

