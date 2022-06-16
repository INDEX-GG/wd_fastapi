from fastapi import APIRouter,File, UploadFile, HTTPException
from typing import List
from app.schemas import response as response_schema
import datetime


router = APIRouter(prefix="",
                   tags=["Upload"])

@router.post("/upload",
             responses={400: {"model": response_schema.ResponseCustomError}})
async def upload(files: List[UploadFile] = File(...)):
    if (len(files) > 3):
        raise HTTPException(
            status_code=400,
            detail="a lot of files.",
        )
    for file in files:
        try:
            contents = await file.read()
            with open("./files/" +datetime.datetime.now().strftime('%m%d%Y') + file.filename, 'wb') as f:
                await f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file(s)"}
        finally:
            await file.close()
    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}