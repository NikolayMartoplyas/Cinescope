from constants import AUTH_URL, ENDPOINT_USER
from custom_requester.custom_requester import CustomRequester

class UserApi(CustomRequester):
    """Класс для получения информации о пользователе"""

    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_URL)

    def get_user_info(self, user_id, expected_status):
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f"{ENDPOINT_USER}/{user_id}",
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status):
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"{ENDPOINT_USER}/{user_id}",
            expected_status=expected_status
        )