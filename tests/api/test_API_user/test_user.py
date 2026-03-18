import allure
import pytest
from models.model_user import User, RegisterUserResponse

@allure.epic("Тестирование пользователя")
@allure.feature("Создание, поиск юзера")
class TestUser:

    @allure.story("Создание пользователя")
    @allure.description("""
    "Этот тест проверяет корректность создания пользователя
    Шаги:
    1. Сощздание пользователя
    2. Валидация структуры ответа
    3. Сравнение полей запроса и ответа
    4. Проверка ID на отсутствие
    5. Проверка поля даты на отсутствие
    """)
    @pytest.mark.movie
    def test_create_user(self, super_admin, create_user_data):
        with allure.step("Создание пользователя"):
            validation_fields = {"email", "fullName", "roles", "verified"}
            response = super_admin.api.user_api.create_user(create_user_data.model_dump())

        with allure.step("Проверка структуры и типов данных ответа"):
            validated_response = RegisterUserResponse.model_validate(response.json())

        with allure.step("Сравнение фактическийц полей ответа с ожидаемыми данными"):
            actual_user = validated_response.model_dump(include=validation_fields, mode="json")
            expected_user = create_user_data.model_dump(include=validation_fields)
            assert actual_user == expected_user

        with allure.step("Проверка ID and createdAt на отсутствие"):
            assert validated_response.id != " ", "ID не может быть пустым"
            assert validated_response.createdAt is not  None, "Поле не может быть пустым"

        with allure.step("Удаление пользователя для освобождения ресурса"):
            super_admin.api.user_api.delete_user(validated_response.id)  # удаление пользователя для освобождения ресурса

    @allure.story("Получение пользователя по локатору")
    @allure.description("""
    Шаги:
    1. Находим пользователя по локатору
    2. Валидируем ответ 
    3. Сравнение полей которые мы отправили и получили в ответ
    4. Проверка ID and createdAt на пустоту
    """)
    @pytest.mark.movie
    def test_get_user_by_locator(self, super_admin, user):
        with allure.step("Поиск пользователя по ID"):
            validation_fields = {"email", "fullName", "roles", "verified", "banned"}
            response = super_admin.api.user_api.get_user_info_by_locator(user.id)

        with allure.step("Проверка структуры и типов данных ответа"):
            validated_response = RegisterUserResponse.model_validate(response.json())

        with allure.step("Сравнение фактическийц полей ответа с ожидаемыми данными"):
            actual = validated_response.model_dump(include=validation_fields, mode="json")
            expected = user.model_dump(include=validation_fields)
            assert actual == expected

        with allure.step("Проверка ID and createdAt на отсутствие"):
            assert validated_response.id != " ", "ID не может быть пустым"
            assert validated_response.createdAt is not None, "Полене модет быть пустым"

    @allure.story("Получение информации о пользователе с ролью USER")
    @allure.description("""
    Шаги:
    1. Поиск пользователя по ID
    2. Проверка ответа сообщения
    """)
    @pytest.mark.movie
    def test_get_user_by_id_common_user(self, common_user, create_user_data):
        with allure.step("Получение информации о пользователе по ID"):
            response = common_user.api.user_api.get_user_info_by_locator(common_user.email, 403)

        with allure.step("Получения сообщения и сравнение его с ожидаемым результатом"):
            message = response.json().get("message")
            assert message == "Forbidden resource", "неверный код ошибки"

