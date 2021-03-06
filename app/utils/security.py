from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from google.oauth2 import id_token
from google.auth.transport import requests
import hashlib
import datetime
from passlib.context import CryptContext
from app.core.config import settings
from app.api import dependencies
from app.schemas import request as request_schema, token as token_schema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.ACCESS_TOKEN_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_TOKEN_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_email_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.EMAIL_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.EMAIL_TOKEN_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_refresh_token(refresh_token: str = Depends(dependencies.oauth2_scheme)):
    try:
        payload = jwt.decode(refresh_token, settings.REFRESH_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
        try:
            user_id = int(user_id)
        except Exception:
            return credentials_exception
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    token_data = {"sub": "user", "user_id": str(payload.get("user_id"))}
    return token_data


def decode_access_token(access_token: str = Depends(dependencies.oauth2_scheme)):
    try:
        payload = jwt.decode(access_token, settings.ACCESS_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
        try:
            user_id = int(user_id)
        except Exception:
            return credentials_exception
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    token_data = {"sub": "user", "user_id": str(payload.get("user_id"))}
    return token_data


def decode_access_token_optional(access_token: str = Depends(dependencies.oauth2_scheme_optional)):
    try:
        payload = jwt.decode(access_token, settings.ACCESS_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
        try:
            user_id = int(user_id)
        except Exception:
            return False
        if user_id is None:
            return False
    except Exception:
        return False
    token_data = {"sub": "user", "user_id": str(payload.get("user_id"))}
    return token_data


def decode_email_token(password_reset_token: str):
    try:
        payload = jwt.decode(password_reset_token, settings.EMAIL_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
    except Exception:
        return False
    return payload


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def decode_google_token(token: str):
    try:
        payload = id_token.verify_oauth2_token(token, requests.Request(), settings.google_Client_ID)
        token_info = token_schema.GoogleTokenData(**payload)
        return token_info
    except Exception:
        return False


def check_vk_data(vk_data: request_schema.RequestVkData):
    check_string = str(settings.vk_app_id) + str(vk_data.auth_data.uid) + str(settings.vk_Secure_Key)
    check_string_md5 = hashlib.md5(check_string.encode()).hexdigest()
    if check_string_md5 != vk_data.auth_data.hash:
        return False
    return True


def decode_apple_token(token: str):
    try:
        payload = jwt.get_unverified_claims(token)
        token_info = token_schema.AppleTokenData(**payload)
        return token_info
    except Exception:
        return False
