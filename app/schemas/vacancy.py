from pydantic import BaseModel
import datetime
from typing import List


class VacancyUser(BaseModel):
    id: int
    name: str | None = None
    surname: str | None = None
    photo: str | None = None


class VacancyFile(BaseModel):
    id: int
    filename: str | None = None


class VacancyBase(BaseModel):
    id: int
    title: str
    description: str | None = None
    budget: int | None = None
    name: str | None = None
    email: str | None = None
    phone: int | None = None
    date: datetime.datetime | None = None


class VacancyOut(VacancyBase):
    user: VacancyUser
    files: List[VacancyFile] | List = []

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
