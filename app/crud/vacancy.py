import datetime
from typing import List
from sqlalchemy.orm import Session
from enum import Enum
import os
from app.db.db_models import Vacancy, File
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


def get_vacancy_by_id_and_user_id(db: Session, vacancy_id: int, user_id: int):
    db_vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id, Vacancy.userId == user_id).first()
    if db_vacancy:
        return db_vacancy
    else:
        return False


def delete_vacancy_by_id(db: Session, vacancy: Vacancy):
    if vacancy:
        db.delete(vacancy)
        db.commit()


def get_vacancy_out(vacancy: Vacancy, files: List[File]):
    vacancy_dict = vacancy.__dict__
    vacancy_dict["user"] = vacancy.user.__dict__
    files_dicts = [i.__dict__ for i in files if os.path.exists(i.patch)]
    vacancy_dict["files"] = files_dicts
    vacancy_out = vacancy_schema.VacancyOut(**vacancy_dict)
    return vacancy_out
