from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud import user as crud_user
from app.schemas import request as request_schema, \
    response as response_schema, token as token_schema
from app.utils import security


router = APIRouter(prefix="",
                   tags=["Login"])


@router.get("/refresh", response_model=token_schema.AccessToken, tags=[], summary="Refresh token")
async def refresh(refresh_token_data: dict = Depends(security.decode_refresh_token)):
    access_token = security.create_access_token(refresh_token_data)
    return {"accessToken": access_token, "tokenType": "bearer"}


@router.post("/login", response_model=response_schema.ResponseLogin, tags=[], summary="",
             responses={400: {"model": response_schema.ResponseCustomError}})
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    user = crud_user.authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    token_data = {"sub": "user", "user_id": str(user.id)}
    access_token = security.create_access_token(data=token_data)
    refresh_token = security.create_refresh_token(data=token_data)
    return {"accessToken": access_token, "refreshToken": refresh_token, "tokenType": "bearer"}


@router.post("/login_google", response_model=response_schema.ResponseLogin, tags=[], summary="Sign in with Google",
             responses={400: {"model": response_schema.ResponseCustomError}})
async def login_google(google_data: request_schema.RequestGoogleData,
                       db: Session = Depends(get_db)):
    token_data = security.decode_google_token(str(google_data.token))
    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    google_id = token_data["sub"]
    print(token_data)
    print(google_id)


@router.post("/login_vk", response_model=response_schema.ResponseLogin, tags=[], summary="Sign in with VK",
             responses={400: {"model": response_schema.ResponseCustomError}})
async def login_google(vk_data: request_schema.RequestVkData,
                       db: Session = Depends(get_db)):
    if not security.check_vk_data(vk_data):
        raise HTTPException(status_code=400, detail="Invalid data")
    vk_id = vk_data.auth_data.uid
    print(vk_data.auth_data)
    print(vk_id)
