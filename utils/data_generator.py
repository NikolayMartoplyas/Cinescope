import datetime
import random
import string
from faker import Faker
from models.model_movies import MoviesModel

faker = Faker()

class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{random_string}@gmail.com"

    @staticmethod
    def generate_random_full_name():
        return f'{faker.first_name()} {faker.last_name()}'

    @staticmethod
    def generate_random_password():
        letters = random.choice(string.ascii_letters)  # Одна буква
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Остальная длина пароля
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generete_random_movie() -> MoviesModel:
        """Генератор афиши фильма"""
        return MoviesModel(
            name=f"{faker.company()} - {faker.catch_phrase()}",
            imageUrl= "https://image.url",
            price= faker.random_int(100, 1000),
            description= faker.text(max_nb_chars=100),
            location= random.choice(["MSK", "SPB"]),
            published= faker.boolean(),
            genreId= faker.random_int(1, 10)
        )

    @staticmethod
    def generete_random_movie_in_db():
        """Генератор афиши фильма для БД"""
        return {
            "name": f"{faker.company()} - {faker.catch_phrase()}",
            "image_url": "https://image.url",
            "price": faker.random_int(100, 1000),
            "description": faker.text(max_nb_chars=100),
            "location": random.choice(["MSK", "SPB"]),
            "published": faker.boolean(),
            "rating": faker.random_int(1, 10),
            "genre_id": faker.random_int(1, 10),
            "created_at": datetime.datetime.now()
        }

    @staticmethod
    def review():
        """Генератор текста для отзыва"""
        return faker.paragraph(nb_sentences=2)

