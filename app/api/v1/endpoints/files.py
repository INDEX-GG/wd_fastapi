from fastapi.responses import FileResponse
from fastapi import File, UploadFile, APIRouter,Depends

from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud.file import get_file,get_files

router = APIRouter(prefix="",
                   tags=["Files"])

@router.get("/files/{vacancy_id}/{file_id}")
async def donwload_file(vacancy_id :int,file_id: int,db: Session = Depends(get_db)):
     return FileResponse(get_file(db,file_id).link)


@router.get("/files/{vacancy_id}")
async def donwload_file(vacancy_id :int, db: Session = Depends(get_db)):
     return (get_files(db,vacancy_id))