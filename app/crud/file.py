from sqlalchemy.orm import Session
from app.db.db_models import File


def create_file_to_db(db: Session, path: str, vacancy_id: int):
    db_file = File(link=path, vacancyId=vacancy_id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def get_files(db: Session, vacancy_id: int):
    query = db.query(File)
    query = query.filter(File.vacancyId == vacancy_id)
    return query.all()


def get_file(db: Session, file_id: int):
    return db.query(File).get(file_id)
