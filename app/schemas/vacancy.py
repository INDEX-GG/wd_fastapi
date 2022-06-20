from typing import List
from pydantic import BaseModel
import datetime


class VacancyBase(BaseModel):
    id: int
    title: str
    description: str | None=None
    budget: int | None = None
    name: str | None = None
    email: str | None = None
    phone: int | None = None
    date: datetime.datetime | None = None
    #files: List[str] | None= None

class VacancyOut(BaseModel):
    vacancies_id: int
    vacancies_title: str
    #description: str | None = None
    #budget: int | None = None
    #name: str | None = None
    #email: str | None = None
    #phone: int | None = None
    #date: datetime.datetime | None = None

    class Config:
        orm_mode = True
#work
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
