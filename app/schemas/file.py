from pydantic import BaseModel


class File(BaseModel):
    link: str
    vacancy_id: int
