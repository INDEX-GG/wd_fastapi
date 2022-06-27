from pydantic import BaseModel
from typing import List


class ShoutoutBase(BaseModel):
    id : int
    rating: int | None
    text: str | None

    id_reviewer : int



class UpdateShoutout(BaseModel):
    rating: int | None
    text: str | None

    id_reviewer: int

class CreateShoutout(BaseModel):
    rating: int
    text: str | None
    in_regard_to : int

class Shoutouts(BaseModel):
    arrSchoutouts : List [ShoutoutBase]
    class Config:
        orm_mode = True


