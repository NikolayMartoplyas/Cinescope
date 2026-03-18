import os
from dotenv import load_dotenv

load_dotenv()

class MoviesDbCreds:
    DB_MOVIES_NANE = os.getenv("DB_MOVIES_NAME")
    DB_MOVIES_USER = os.getenv("DB_MOVIES_USER")
    DB_MOVIES_PASSWORD = os.getenv("DB_MOVIES_PASSWORD")
    DB_MOVIES_HOST = os.getenv("DB_MOVIES_HOST")
    DB_MOVIES_PORT = os.getenv("DB_MOVIES_PORT")