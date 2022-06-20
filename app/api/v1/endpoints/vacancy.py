from fastapi import APIRouter, UploadFile, HTTPException, Depends, File
from typing import List, Optional
import uuid
from app.api.dependencies import get_db
from app.crud import vacancy as crud_vacancy
from app.crud import file as crud_file
from app.schemas import vacancy as vacancy_schema
from sqlalchemy.orm import Session
import os


router = APIRouter(prefix="/vacancies",
                   tags=["Vacancies"])


@router.get("/vacancies/{vacancy_id}")
async def get_vacancy_by_id(vacancy_id: int, db: Session = Depends(get_db)):
    db_vacancy = crud_vacancy.get_vacancy_by_id(db, vacancy_id)
    file_list = crud_file.get_files(db, vacancy_id)
    return {"vacancy": db_vacancy,
            "links": file_list}


@router.post("/vacancies", summary=" create vacancy  & Uploads files")
async def create_vacancy(vacancy: vacancy_schema.VacancyCreate = Depends(),
                         files: Optional[List[UploadFile]] = File(None),
                         db: Session = Depends(get_db)):
    if len(files) > 3:
        raise HTTPException(status_code=400, detail="a lot of files")
    new_vacancy = crud_vacancy.create_vacancy(db=db, vacancy=vacancy)
    path = "./files/" + str(new_vacancy.id) + "/"
    os.mkdir(path)
    for file in files:
        try:
            with open(path + str(uuid.uuid1()) + file.filename, "wb+") as f:
                contents = await file.read()
                f.write(contents)
                crud_file.create_file_to_db(db, f.name, new_vacancy.id)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="uploading the file(s) error")
    return new_vacancy
