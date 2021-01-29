from model.base import Base
from database.database_session import engine

Base.metadata.create_all(bind=engine)