"""Defined a database session"""

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import config_settings

SQLALCHEMY_DATABASE_URL = config_settings.POSTGRES_URI

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# return database session class, we can create session instance to be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db_session():
    try:
        db = SessionLocal()
        yield db
        db.close()
    except Exception:
        db.rollback()
        raise
