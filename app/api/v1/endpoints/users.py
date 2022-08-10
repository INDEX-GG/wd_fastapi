from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud import user as crud_user
from app.schemas import user as user_schema, response as response_schema


router = APIRouter(prefix="/users",
                   tags=["Users"])


@router.post("", response_model=response_schema.ResponseSuccess, tags=[], summary="Registration user",
             description="", status_code=201, responses={409: {"model": response_schema.ResponseCustomError}})
async def registration(user: user_schema.UserCreate,
                       db: Session = Depends(get_db)):
    new_user = crud_user.create_user(user=user, db=db)
    if not new_user:
        raise HTTPException(status_code=409, detail="User with this email already exist")
    return {"message": "success"}


@router.get("/me", response_model=user_schema.UserOut, tags=[], summary="Get User Me")
async def read_users_me(current_user: user_schema.UserOut = Depends(crud_user.get_current_user)):
    return current_user


@router.put("/me",
            response_model=response_schema.ResponseSuccess,
            tags=[], summary="Change User Me")
async def read_users_me(new_user_data: user_schema.ChangeUser,
                        db: Session = Depends(get_db),
                        current_db_user=Depends(crud_user.get_current_db_user)):
    if new_user_data.email:
        if not crud_user.check_email_exist(user_data=new_user_data, db=db):
            raise HTTPException(status_code=409, detail="User with this email already exist")
    if new_user_data.phone:
        if not crud_user.check_phone_exist(user_data=new_user_data, db=db):
            raise HTTPException(status_code=409, detail="User with this phone already exist")
    crud_user.change_user_data(user=current_db_user, user_data=new_user_data, db=db)
    return {"message": "success"}
