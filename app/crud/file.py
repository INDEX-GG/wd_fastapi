from fastapi import UploadFile, File, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
import aiofiles
import os
import uuid
from app.db.db_models import File as DbFile


def create_file_to_db(db: Session, patch: str, vacancy_id: int, filename: str):
    db_file = DbFile(patch=patch,
                     filename=filename,
                     vacancyId=vacancy_id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


async def save_files(db: Session, vacancy_id: int, files: Optional[List[UploadFile]] = File(None)):
    if files:
        if len(files) > 3:
            raise HTTPException(status_code=400, detail="a lot of files")
        for file in files:
            try:
                file_patch = "./files/{}/{}/".format(vacancy_id, uuid.uuid4())
                if not os.path.exists(file_patch):
                    os.makedirs(file_patch)
                async with aiofiles.open("{}{}".format(file_patch, file.filename), mode="wb+") as f:
                    content = await file.read()
                    await f.write(content)
                    create_file_to_db(db=db, patch="{}{}".format(file_patch, file.filename),
                                      vacancy_id=vacancy_id, filename=file.filename)
            except Exception:
                pass


def get_files(db: Session, vacancy_id: int):
    db_files = db.query(DbFile).filter(DbFile.vacancyId == vacancy_id).all()
    return db_files


def get_file(db: Session, file_id: int):
    db_file: DbFile = db.query(DbFile).filter(DbFile.id == file_id).first()
    if not db_file:
        return False
    return db_file
