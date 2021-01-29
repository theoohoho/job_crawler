"""Defined Datbase Session"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import config_settings
SQLALCHEMY_DATABASE_URL = config_settings.POSTGRES_URI
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# sqlite_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# return database session class, we can create session instance to be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
    finally:
        db.close()
