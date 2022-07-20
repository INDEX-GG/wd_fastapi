import datetime

from pydantic import BaseModel, Field


class Shoutout(BaseModel):
    id: int
    userId: int
    text: str
    rating: int = Field(..., ge=0, le=5)
    createdAt: datetime.datetime


class CreateShoutout(BaseModel):
    text: str
    rating: int = Field(..., ge=0, le=5)
