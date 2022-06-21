from fastapi import UploadFile, File, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
import aiofiles
import os
import uuid
from app.db.db_models import File as DbFile


def create_file_to_db(db: Session, path: str, vacancy_id: int, filename: str):
    db_file = DbFile(link=path,
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
                    create_file_to_db(db=db, path="{}{}".format(file_patch, file.filename),
                                      vacancy_id=vacancy_id, filename=file.filename)
            except Exception:
                pass


def get_files(db: Session, vacancy_id: int):
    query = db.query(DbFile)
    query = query.filter(DbFile.vacancyId == vacancy_id)
    return query.all()


def get_file(db: Session, file_id: int):
    return db.query(DbFile).get(file_id)
