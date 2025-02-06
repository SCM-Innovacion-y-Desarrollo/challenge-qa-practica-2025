from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta

from src.schemas import InputModel


def get_all(db: Session, model: DeclarativeMeta, **kwargs) -> List[DeclarativeMeta]:
    query = db.query(model)
    return query.all()


def get_by_id(db: Session, model: DeclarativeMeta, id: int) -> DeclarativeMeta:
    data = db.query(model).get(id)
    return data


def create(db: Session, model: DeclarativeMeta, data: InputModel) -> DeclarativeMeta:
    new_data = model(**data.__dict__)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data
