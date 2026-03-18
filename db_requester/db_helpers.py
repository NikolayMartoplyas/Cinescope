from sqlalchemy.orm import Session
from db_models.user import UserDBModel
from db_models.movie import MovieDBModel

class DBHelperUser:
    """Класс с методами для работы с БД в тестах"""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_test_user(self, user_data: dict) -> UserDBModel:
        """Метод для создания пользователя в БД"""
        user = UserDBModel(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user_by_id(self, user_id: str):
        """Получение пользователя по ID из БД"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.id == user_id).first()

    def get_user_by_email(self, email: str):
        """Получение пользователя по Email из БД"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).first()

    def user_exists_by_email(self, email: str):
        """Проверяет сущевствоние пользовтеля по Email"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).count() > 0

    def delete_user(self, user: UserDBModel):
        """Удаляет пользователя"""
        self.db_session.delete(user)
        self.db_session.commit()

    def cleanup_test_data(self, objects_to_delete: list):
        """Очищает тестовые данные"""
        for obj in objects_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()

class DBHelperMovies:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_movie_in_db(self, movie_data: dict) -> MovieDBModel:
        """Создание фильма в БД"""
        movie = MovieDBModel(**movie_data)
        self.db_session.add(movie)
        self.db_session.commit()
        self.db_session.refresh(movie)
        return movie

    def get_movie_by_id(self, movie_id: str):
        """Получение фильма по ID из БД"""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.id == movie_id).first()

    def delete_movie(self, movie: MovieDBModel):
        """Удаление фильма из БД"""
        self.db_session.delete(movie)
        self.db_session.commit()

