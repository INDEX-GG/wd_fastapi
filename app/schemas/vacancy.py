from pydantic import BaseModel
import datetime


class VacancyBase(BaseModel):
    id: int
    title: str
    description: str | None = None
    budget: int | None = None
    name: str | None = None
    email: str | None = None
    phone: int | None = None
    date: datetime.datetime | None = None


class VacancyOut(BaseModel):
    vacancies_id: int
    vacancies_title: str

    class Config:
        orm_mode = True


class VacancyCreate(BaseModel):
    title: str
    description: str | None = None
    budget: int | None = None
    name: str | None = None
    email: str | None = None
    phone: int | None = None

    class Config:
        orm_mode = True
