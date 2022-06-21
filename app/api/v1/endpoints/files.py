from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from app.api.dependencies import get_db
from app.crud import file as file_crud
from app.schemas import response as response_schema


router = APIRouter(prefix="/files",
                   tags=["Files"])


@router.get("/{file_id}",
            summary="Get File Of Vacancy",
            response_class=FileResponse,
            status_code=200,
            responses={404: response_schema.custom_errors("Bad Request", ["file not found"])})
async def download_file(file_id: int,
                        db: Session = Depends(get_db)):
    file = file_crud.get_file(db=db, file_id=file_id)
    if not file:
        raise HTTPException(status_code=404, detail="file not found")
    if not os.path.exists(file.patch):
        raise HTTPException(status_code=404, detail="file not found")
    return FileResponse(file.patch, media_type="application/octet-stream", filename=file.filename)
