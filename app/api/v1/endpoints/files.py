from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud.file import get_file, get_files

router = APIRouter(prefix="/files",
                   tags=["Files"])


@router.get("/{vacancy_id}/{file_id}")
async def download_file(file_id: int, db: Session = Depends(get_db)):
    return FileResponse(get_file(db, file_id).link)


@router.get("/{vacancy_id}")
async def download_file(vacancy_id: int, db: Session = Depends(get_db)):
    return get_files(db, vacancy_id)
