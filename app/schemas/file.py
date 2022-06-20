from pydantic import BaseModel

class File(BaseModel):
    link : str
    vacansy_id: int

