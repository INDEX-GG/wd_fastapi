from fastapi import APIRouter, UploadFile, Depends, File, HTTPException
from fastapi.responses import FileResponse
from typing import List, Optional
from app.api.dependencies import get_db
from app.crud import vacancy as vacancy_crud, file as file_crud, user as user_crud
from app.schemas import vacancy as vacancy_schema, response as response_schema, user as user_schema
from sqlalchemy.orm import Session


router = APIRouter(prefix="/vacancies",
                   tags=["Vacancies"])


@router.get("/{vacancy_id}", summary="Get Vacancy By Id",
            response_model=vacancy_schema.VacancyOut,
            status_code=200,
            responses={404: response_schema.custom_errors("Bad Request", ["vacancy not found"])})
async def get_vacancy_by_id(vacancy_id: int, db: Session = Depends(get_db)):
    db_vacancy = vacancy_crud.get_vacancy_by_id(db, vacancy_id)
    if not db_vacancy:
        raise HTTPException(status_code=404, detail="vacancy not found")
    vacancy_files = file_crud.get_files(db, vacancy_id)
    vacancy_out = vacancy_crud.get_vacancy_out(vacancy=db_vacancy, files=vacancy_files)
    return vacancy_out


@router.post("", summary="Create Vacancy", response_model=response_schema.ResponseSuccess,
             status_code=201,
             responses={400: response_schema.custom_errors("Bad Request", ["a lot of files"])})
async def create_vacancy(vacancy: vacancy_schema.VacancyCreate = Depends(),
                         files: Optional[List[UploadFile]] = File(None),
                         current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                         db: Session = Depends(get_db)):
    new_vacancy = vacancy_crud.create_vacancy(db=db, vacancy=vacancy, user_id=current_user.id)
    await file_crud.save_files(db=db, files=files, vacancy_id=new_vacancy.id)
    return {"message": "success"}
