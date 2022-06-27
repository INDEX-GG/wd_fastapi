from pydantic import BaseModel
from typing import List

class CreateHistorySeqrch(BaseModel):
    searchQuery : str
    flagPrice : bool | None = False
    price : int | None = 0

class ListHistory(BaseModel):
    arrHistory : List[CreateHistorySeqrch]