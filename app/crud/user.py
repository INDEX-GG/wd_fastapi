from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
import uuid
import datetime
from app.api.dependencies import get_db
from app.api import dependencies
from app.db.db_models import User
from app.schemas import user as user_schema
from app.utils import security


def get_current_user(db: Session = Depends(get_db), access_token: str = Depends(dependencies.oauth2_scheme)):
    token_data = security.decode_access_token(access_token)
    user_id = token_data["user_id"]
    user = get_user(db=db, user_id=user_id)
    if user is None:
        raise security.credentials_exception
    return user


async def get_current_email_verify_user(current_user: user_schema.UserOut = Depends(get_current_user)):
    if not current_user.emailVerified:
        raise HTTPException(status_code=400, detail="not email verified")
    return current_user


def authenticate_user(db: Session, username: str, password: str):
    db_user = db.query(User).filter(User.email == username).first()
    if not db_user:
        return False
    if not security.verify_password(password, db_user.password):
        return False
    return db_user


def get_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        user_dict = db_user.__dict__
        user_dict["role"] = db_user.role.__dict__
        if db_user.photo:
            user_dict["photo"] = db_user.photo.__dict__
        user = user_schema.UserOut(**user_dict)
        return user
    else:
        return False


def get_user_by_email(db: Session, email: str):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        return db_user
    else:
        return False


def create_user(db: Session, user: user_schema.UserCreate):
    instance = db.query(User).filter(User.email == user.email).first()
    if instance:
        return False
    else:
        db_user = User(uuid=uuid.uuid4(),
                       email=user.email,
                       name=user.name,
                       emailVerified=False,
                       phoneVerified=False,
                       password=security.hash_password(user.password),
                       roleId=1,
                       createdAt=datetime.datetime.utcnow())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        user_dict = db_user.__dict__
        user_dict["role"] = db_user.role.__dict__
        if db_user.photo:
            user_dict["photo"] = db_user.photo.__dict__
        user = user_schema.UserOut(**user_dict)
        return user


def change_user_password(db: Session, user: User, new_password: str):
    user.password = new_password
    db.commit()
