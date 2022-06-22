from typing import List
from pydantic import BaseModel
import datetime


class PostCreate(BaseModel):
    title: str
    description: str | None = None
    priceAmount: int | None = None
    priceCurrency: str | None = None

    class Config:
        orm_mode = True


class PostsBase(BaseModel):
    title: str
    description: str | None = None
    priceAmount: int | None = None
    priceCurrency: str | None = None
    link: str | None = None
    date: datetime.datetime | None = None
    source: str | None = None
    parseDate: str | None = None


class Post(PostsBase):
    id: int

    class Config:
        orm_mode = True


class Posts(BaseModel):
    posts: List[Post]
    postsCount: int | None = None

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    id: int

    class Config:
        orm_mode = True