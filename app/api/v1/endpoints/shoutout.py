from fastapi import APIRouter, Depends, Query
from typing import List
from app.api.dependencies import get_db
from sqlalchemy.orm import Session
from app.schemas import user as user_schema, shoutout as shoutout_schema, response as response_schema
from app.crud import user as user_crud, shoutout as shoutout_crud


router = APIRouter(prefix="/shoutouts", tags=["shoutout"])


@router.post("", summary="create shoutout",
             response_model=response_schema.ResponseSuccess, status_code=201)
async def create_shoutout(shoutout: shoutout_schema.CreateShoutout,
                          current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                          db: Session = Depends(get_db)):
    shoutout_crud.create_shoutout(db=db, shoutout=shoutout, user_id=current_user.id)
    return {"msg": "success"}


@router.get("/my", summary="Get user shoutouts page by page",
            response_model=List[shoutout_schema.ShoutoutOut])
async def get_user_shoutouts(current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                             page: int = Query(default=1, ge=1, le=1000),
                             page_limit: int = Query(alias="pageLimit", default=60, ge=1, le=200),
                             db: Session = Depends(get_db)):
    list_user_shoutouts = shoutout_crud.read_user_shoutouts(db=db,
                                                            user_id=current_user.id,
                                                            page_limit=page_limit,
                                                            page=page)
    shoutouts_out = shoutout_crud.get_shoutouts_out(list_user_shoutouts)
    return shoutouts_out


@router.get("", summary="Get all shoutouts page by page",
            response_model=List[shoutout_schema.ShoutoutOut])
async def get_user_shoutouts(page: int = Query(default=1, ge=1, le=1000),
                             page_limit: int = Query(alias="pageLimit", default=60, ge=1, le=200),
                             db: Session = Depends(get_db)):
    list_all_shoutouts = shoutout_crud.read_all_shoutouts(db=db,
                                                          page_limit=page_limit,
                                                          page=page)
    shoutouts_out = shoutout_crud.get_shoutouts_out(list_all_shoutouts)
    return shoutouts_out
