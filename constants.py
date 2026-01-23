import os
from dotenv import load_dotenv

load_dotenv()
AUTH_EMAIL = os.getenv("AUTH_EMAIL")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")

MOVIE_URL = "https://api.dev-cinescope.coconutqa.ru"
AUTH_URL = "https://auth.dev-cinescope.coconutqa.ru"
ENDPOINT_MOVIES = "/movies"
ENDPOINT_LOGIN = "/login"
ENDPOINT_REGISTER = "/register"
ENDPOINT_USER = "/user"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

AUTH_DATE = {
    "email": AUTH_EMAIL,
    "password": AUTH_PASSWORD
}