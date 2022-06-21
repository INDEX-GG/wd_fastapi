import datetime

from sqlalchemy.orm import Session
from enum import Enum
from app.db.db_models import Vacancy
from app.schemas import vacancy as vacancy_schema


class SortValues(str, Enum):
    default = "default"
    new = "new"
    cheaper = "cheaper"
    expensive = "expensive"


def create_vacancy(db: Session,  vacancy: vacancy_schema.VacancyCreate, user_id: int):
    db_vacancy = Vacancy(userId=user_id,
                         title=vacancy.title,
                         description=vacancy.description,
                         budget=vacancy.budget,
                         name=vacancy.name,
                         email=vacancy.email,
                         phone=vacancy.phone,
                         createdAt=datetime.datetime.utcnow())
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy


def get_vacancy_by_id(db: Session, vacancy_id: int):
    db_vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if db_vacancy:
        return db_vacancy
    else:
        return False
