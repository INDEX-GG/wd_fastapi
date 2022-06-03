from pydantic import BaseModel
from uuid import UUID
import datetime


class UserRole(BaseModel):
    id: int
    title: str


class UserPhoto(BaseModel):
    id: int
    url: str


class UserCreate(BaseModel):
    email: str
    password: str
    name: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str | None = None
    phone: int | None = None
    name: str | None = None
    surname: str | None = None
    username: str | None = None
    photo: int | None = None
    rating: int | None = None
    role: int | None = None
    google_id: int | None = None
    vk_id: int | None = None
    apple_id: int | None = None
    updatedAt: datetime.datetime | None = None
    lastLoginAt: datetime.datetime | None = None
    deletedAt: datetime.datetime | None = None
    emailVerifiedAt: datetime.datetime | None = None
    phoneVerifiedAt: datetime.datetime | None = None

    class Config:
        orm_mode = True


class UserOut(UserBase):
    id: int
    uuid: UUID
    email: str
    emailVerified: bool
    phoneVerified: bool
    createdAt: datetime.datetime
    photo: UserPhoto | None = None
    role: UserRole

    class Config:
        orm_mode = True
