from pydantic import BaseModel
from typing import List


class Favorite(BaseModel):
    id: int
    userId: int
    objId: int


class CreateFavorite(BaseModel):
    userId: int
    objId: int


class Favorites(Favorite):
    arrFav: List[Favorite]

    class Config:
        orm_mode = True
