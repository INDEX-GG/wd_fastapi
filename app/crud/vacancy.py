from sqlalchemy import or_, nullslast
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

def get_vacancy_by_id (db: Session, id: str):
    return db.query(Vacancy).filter(Vacancy.id == id)


def get_vacancies_page_by_page (
                            db: Session,
                            page: int = 1,
                            page_limit: int = 60,
                            price_from: int = None,
                            with_contract_price: bool = None,
                            search_string: str = None,
                            sort: SortValues = "default"):
    offset = (page - 1) * page_limit
    query = db.query(Vacancy)
    vacancies_count = None
    if price_from:
        if with_contract_price:
            query = query.filter(or_(Vacancy.budget >= price_from, Vacancy.budget == None))
        else:
            query = query.filter(Vacancy.budget >= price_from)
    if search_string:
        query = query.filter(Vacancy.title.ilike("%" + search_string + "%"))
    match sort:
        case SortValues.default.name:
            query = query.order_by(Vacancy.date.desc())
        case SortValues.new.name:
            query = query.order_by(Vacancy.date.desc())
        case SortValues.cheaper.name:
            query = query.order_by(nullslast(Vacancy.budget.asc()))
        case SortValues.expensive.name:
            query = query.order_by(nullslast(Vacancy.budget.desc()))

    if page == 1:
        vacancies_count = query.count()
    vacancies = query.offset(offset).limit(page_limit).all()
    return vacansy_schema.Vacancy(vacancies=vacancies, vacanciesCount=vacancies_count)