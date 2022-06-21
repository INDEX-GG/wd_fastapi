from fastapi import APIRouter, UploadFile, HTTPException, Depends, File
from typing import List, Optional
from app.api.dependencies import get_db
from app.crud import vacancy as vacancy_crud, file as file_crud, user as user_crud
from app.schemas import vacancy as vacancy_schema, response as response_schema, user as user_schema
from sqlalchemy.orm import Session


router = APIRouter(prefix="/vacancies",
                   tags=["Vacancies"])


@router.get("/{vacancy_id}")
async def get_vacancy_by_id(vacancy_id: int, db: Session = Depends(get_db)):
    db_vacancy = vacancy_crud.get_vacancy_by_id(db, vacancy_id)
    file_list = file_crud.get_files(db, vacancy_id)
    return {"vacancy": db_vacancy,
            "links": file_list}


@router.post("", summary=" create vacancy  & Uploads files", response_model=response_schema.ResponseSuccess,
             status_code=201,
             responses={400: response_schema.custom_errors("Bad Request", ["a lot of files"])})
async def create_vacancy(vacancy: vacancy_schema.VacancyCreate = Depends(),
                         files: Optional[List[UploadFile]] = File(None),
                         current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                         db: Session = Depends(get_db)):
    new_vacancy = vacancy_crud.create_vacancy(db=db, vacancy=vacancy, user_id=current_user.id)
    await file_crud.save_files(db=db, files=files, vacancy_id=new_vacancy.id)
    return {"message": "success"}
