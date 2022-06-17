from fastapi import APIRouter,File, UploadFile, HTTPException, Query, Depends, Form
from typing import List
import uuid
from app.api.dependencies import get_db
from app.crud import vacancy as crud_vacancy
from app.schemas import vacancy as vacansy_schema , file as file_schema
from app.db.db_models import File as F
from sqlalchemy.orm import Session
import os


router = APIRouter(prefix="",
                   tags=["Vacancies"])

@router.get("/vacancies", response_model=vacansy_schema.Vacancies, tags=[], summary="Get vacancies page by pages", description="")
async def get_vacancies_page_by_page(
        page: int = Query(default=1, ge=1, le=1000),
        page_limit: int = Query(alias="pageLimit", default=60, ge=1, le=200),
        price_from: int = Query(alias="priceFrom", default=None, ge=0, le=1000000000000),
        with_contract_price: bool = Query(alias="withContractPrice", default=None),
        search_string: str = Query(alias="searchString", default=None, min_length=1, max_length=200),
        sort: crud_vacancy.SortValues = Query(default="default"),
        db: Session = Depends(get_db)):
    items = crud_vacancy.get_vacancies_page_by_page(db=db,
                                                   page=page,
                                                   page_limit=page_limit,
                                                   price_from=price_from,
                                                   with_contract_price=with_contract_price,
                                                   search_string=search_string,
                                                   sort=sort)
    return items

@router.get("/vacancies/{vacancy_id}", response_model=vacansy_schema.Vacancies)
async def get_vacancy_by_id( vacancy_id :int , db: Session = Depends(get_db) ):
    db_vacancy = crud_vacancy.get_vacancy_by_id(db, vacancy_id)
    if db_vacancy is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_vacancy

@router.post("/vacancies", summary=" create vacancy  & Uploads files")
async def create_vacancu( files: List[UploadFile] =  File(...) ,
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
                addFileToDB(db,file_schema,f.name, new_vacancy.id)

        except Exception as E:
            print(E)
            return {"message": "There was an error uploading the file(s)"}
    return new_vacancy


def addFileToDB(db: Session,
                file: file_schema,
                path : str,
                idV : int):
    db_file = F(link=path,
                vacansy_id=idV)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file;
