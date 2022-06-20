from sqlalchemy import or_, nullslast
from sqlalchemy.orm import Session
from enum import Enum
from app.db.db_models import File as F
from app.schemas import file as file_schema

def create_file_to_db(db: Session,
                    path: str,
                    idV: int):
        db_file = F(link=path,
                    vacansy_id=idV)
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        return db_file

def get_files (db: Session,
               vac_id: int):
    q = db.query(F)
    q = q.filter(F.vacansy_id == vac_id)
    return q.all()

def get_file(db: Session, file_id: int):
    return db.query(F).get(file_id)
