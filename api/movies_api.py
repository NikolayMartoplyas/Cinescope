from custom_requester.custom_requester import CustomRequester
from constants import MOVIE_URL, ENDPOINT_MOVIES
class MoviesApi(CustomRequester):

    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIE_URL)

    def get_poster_movie(self, params, expected_status):
        """
        Получение афиши фильма
        :param params: Данные для фильтрации фильмов
        :param expected_status: Ожидаемый статус код
        :return:
        """
        return self.send_request(
            method="GET",
            endpoint=ENDPOINT_MOVIES,
            params=params,
            expected_status=expected_status
        )

    def creating_movie_poster(self, data_movie, expected_status):
        """
        Создание афиши фильма
        :param data_film: данные для создания фильма
        :param expected_status: Ожидаемый статус код
        """
        return self.send_request(
            method="POST",
            endpoint=ENDPOINT_MOVIES,
            data=data_movie,
            expected_status=expected_status
        )

    def get_movie_by_id(self, movie_id, expected_status):
        """
        Получение фильма по ID
        :param movie_id: ID созданного фильма
        :param expected_status: Ожидаемый статус код
        """
        return self.send_request(
            method="GET",
            endpoint=f"{ENDPOINT_MOVIES}/{movie_id}",
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status):
        """
        Удаление фильма по ID
        :param movie_id: ID созданного фильма
        :param expected_status: Ожидаемый статус код
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"{ENDPOINT_MOVIES}/{movie_id}",
            expected_status=expected_status
        )

    def editing_a_movie_by_id(self, movie_id, new_movie, expected_status):
        """
        Редактирование афиши фильма
        :param movie_id: ID созданного фильма
        :param new_movie: Новая афиша фильма
        :param expected_status: Ожидаемый статус код
        """
        return self.send_request(
            method="patch",
            endpoint=f"{ENDPOINT_MOVIES}/{movie_id}",
            data=new_movie,
            expected_status=expected_status
        )