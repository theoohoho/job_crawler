"""A Base crud class"""
from sqlalchemy.orm import Session
from database.base_class import Base
from pydantic import BaseModel
from typing import TypeVar, Generic, Dict, List, Union, Any

ModelType = TypeVar("ModelType", bound=Base)
DataSchemaType = TypeVar("DataSchemaType", bound=BaseModel)


def db_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            raise
    return wrapper


class CRUDBase(Generic[ModelType, DataSchemaType]):
    """Defined crud base class."""

    def __init__(self, model: Base):
        self.model = model

    @db_exception
    def get(self, db: Session, filter_dict: Dict = {}) -> ModelType:
        return db.query(self.model).filter_by(**filter_dict).first()

    @db_exception
    def get_all(self, db: Session, filter_dict: Dict = {}) -> List[ModelType]:
        return db.query(self.model).filter_by(**filter_dict).all()

    @db_exception
    def get_all_pagination(self, db: Session, filter_dict: Dict = {}, offset: int = 0, limit: int = 0,) -> List[ModelType]:
        return db.query(self.model).filter_by(**filter_dict).order_by().offset(offset).limit(limit).all()

    @db_exception
    def create(self, db: Session, obj_in: DataSchemaType) -> ModelType:
        created_obj = self.model(**obj_in.dict())
        db.add(created_obj)
        db.commit()
        db.refresh(created_obj)
        return created_obj

    @db_exception
    def update(self, db: Session, db_obj: ModelType, obj_in: Union[Dict[str, Any], DataSchemaType]) -> ModelType:
        updated_row = obj_in if isinstance(obj_in, dict) else obj_in.dict()
        for key, val in updated_row.items():
            setattr(db_obj, key, val)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @db_exception
    def update_by(self, db: Session, filter_dict: Dict, updated_field: Dict) -> ModelType:
        updated_row = db.query(self.model).filter_by(**filter_dict)
        updated_row.update(updated_field)
        db.commit()
        return updated_row.first()

    @db_exception
    def remove(self,  db: Session, filter_dict: Dict = {}) -> ModelType:
        db_obj = db.query(self.model).filter_by(**filter_dict).first()
        db.delete(db_obj)
        db.commit()
        return db_obj

    @db_exception
    def add_all(self, db: Session, objs_in: List[DataSchemaType]) -> None:
        db_objs = [self.model(**obj.dict()) for obj in objs_in]
        db.add_all(db_objs)
