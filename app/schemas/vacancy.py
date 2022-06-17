from typing import List
from pydantic import BaseModel
import datetime


class VacancyBase(BaseModel):
    user_id : int
    title: str
    description: str | None=None
    budget: int | None = None
    name: str | None = None
    email: str | None = None
    phone: int | None = None
    date: datetime.datetime | None = None
    #files: List[str] | None= None

#из БД
class Vacancy (VacancyBase):
    id: int

    class Config:
        orm_mode = True

class VacancyCreate(BaseModel):
    title: str
    description: str | None = None
    budget: int | None = None
    name: str | None = None
    email: str | None = None
    phone: int | None = None
    #files: List[str] | None = None

    class Config:
        orm_mode : True

class Vacancies (BaseModel):
    vacancies : List[Vacancy]
    vacanciesCount : int | None=None

    class Config:
        orm_mode : True
