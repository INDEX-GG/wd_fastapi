from fastapi import APIRouter,File, UploadFile, HTTPException, Query, Depends, Form
from typing import List
import uuid
from app.api.dependencies import get_db
from app.crud import vacancy as crud_vacancy
from app.crud import file as crud_file

from app.schemas import vacancy as vacansy_schema , file as file_schema
from app.db.db_models import File as F
from sqlalchemy.orm import Session
import os


router = APIRouter(prefix="",
                   tags=["Vacancies"])



@router.get("/vacancies/{vacancy_id}")
async def get_vacancy_by_id(vacancy_id :int, db: Session = Depends(get_db)):
    db_vacancy =crud_vacancy.get_vacancy_by_id(db,vacancy_id)
    file_list = crud_file.get_files(db, vacancy_id)
    return {"vacancy" : db_vacancy,
            "links" : file_list}


@router.post("/vacancies", summary=" create vacancy  & Uploads files")
async def create_vacancy(files:  List[UploadFile] = File(...)  ,
                         vacancy : vacansy_schema.VacancyCreate = Depends(),
                         db: Session = Depends(get_db)):
    new_vacancy = crud_vacancy.create_vacancy( db=db,vacancy = vacancy)

    if len(files) > 3:
        raise HTTPException(status_code=400,detail="a lot of files.")

    path = "./files/" + str(new_vacancy.id) +"/"
    os.mkdir(path)
    for file in files:
        try:
            with open(path+  str(uuid.uuid1()) + file.filename, "wb+") as f:
                contents = await file.read()
                f.write(contents)
                crud_file.create_file_to_db(db,f.name, new_vacancy.id)

        except Exception as E:
            print(E)
            return {"message": "There was an error uploading the file(s)"}
    return new_vacancy

