import datetime
from uuid import UUID
from typing import List

from pydantic import BaseModel, Field


class ShoutoutUser(BaseModel):
    id: int
    uuid: UUID
    name: str | None
    surname: str | None
    username: str | None
    rating: int | None
    photoId: int | None


class ShoutoutOut(BaseModel):
    id: int
    user: ShoutoutUser
    text: str
    rating: int = Field(..., ge=0, le=5)
    createdAt: datetime.datetime


class ShoutoutsOut(BaseModel):
    shoutouts: List[ShoutoutOut]
    shoutoutsCount: int | None = None

    class Config:
        orm_mode = True


class Shoutout(BaseModel):
    id: int
    text: str
    rating: int = Field(..., ge=0, le=5)
    createdAt: datetime.datetime


class CreateShoutout(BaseModel):
    text: str
    rating: int = Field(..., ge=0, le=5)
