from pydantic import BaseModel
from typing import List
import datetime


class CreateHistorySearch(BaseModel):
    searchQuery: str
    withContractPrice: bool | None = False
    price: int | None = None


class HistorySearchOut(BaseModel):
    id: int
    searchQuery: str
    withContractPrice: bool | None = False
    price: int | None = None
    createdAt: datetime.datetime

    class Config:
        orm_mode = True


class ListHistory(BaseModel):
    searchHistory: List[HistorySearchOut]
    searchHistoryCount: int | None = None

    class Config:
        orm_mode = True
