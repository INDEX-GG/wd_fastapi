from sqlalchemy.orm import Session
from enum import Enum
from app.db.db_models import Vacancy
from app.schemas import vacancy as vacansy_schema


class SortValues(str, Enum):
    default = "default"
    new = "new"
    cheaper = "cheaper"
    expensive = "expensive"

def create_vacancy(db: Session,  vacancy : vacansy_schema.VacancyCreate):
    db_vacancy = Vacancy(title=vacancy.title,
                         description=vacancy.description,
                         budget=vacancy.budget,
                         name=vacancy.name,
                         email=vacancy.email,
                         phone=vacancy.phone)

    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy

def get_vacancy_by_id (db: Session, id: int):
    return db.query(Vacancy).get(id)

