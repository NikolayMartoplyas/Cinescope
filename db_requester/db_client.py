from resources.db_creds import MoviesDbCreds
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_MOVIES_NANE = MoviesDbCreds.DB_MOVIES_NANE
DB_MOVIES_USER = MoviesDbCreds.DB_MOVIES_USER
DB_MOVIES_PASSWORD = MoviesDbCreds.DB_MOVIES_PASSWORD
DB_MOVIES_HOST = MoviesDbCreds.DB_MOVIES_HOST
DB_MOVIES_PORT = MoviesDbCreds.DB_MOVIES_PORT

# Движок для подключения к БД

engine = create_engine(
    f"postgresql+psycopg2://{DB_MOVIES_USER}:{DB_MOVIES_PASSWORD}@{DB_MOVIES_HOST}:{DB_MOVIES_PORT}/{DB_MOVIES_NANE}",
    echo=False #установить True для отладки в конслои
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """Создает новую сессию"""
    return SessionLocal()