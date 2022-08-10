from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
import uuid
import datetime
from app.api.dependencies import get_db
from app.api import dependencies
from app.db.db_models import User, Photo
from app.schemas import user as user_schema
from app.utils import security


def get_current_user(db: Session = Depends(get_db), access_token: str = Depends(dependencies.oauth2_scheme)):
    token_data = security.decode_access_token(access_token)
    user_id = token_data["user_id"]
    user = get_user(db=db, user_id=user_id)
    if user is None:
        raise security.credentials_exception
    return user


def get_current_db_user(db: Session = Depends(get_db), access_token: str = Depends(dependencies.oauth2_scheme)):
    token_data = security.decode_access_token(access_token)
    user_id = token_data["user_id"]
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise security.credentials_exception
    return db_user


def get_current_user_optional(db: Session = Depends(get_db),
                              access_token: str = Depends(dependencies.oauth2_scheme_optional)):
    token_data = security.decode_access_token_optional(access_token)
    if token_data:
        user_id = token_data["user_id"]
        user = get_user(db=db, user_id=user_id)
        return user
    return None


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


def get_user_by_google_id(db: Session, google_id: str):
    db_user = db.query(User).filter(User.googleId == google_id).first()
    if db_user:
        return db_user
    else:
        return False


def get_user_by_apple_id(db: Session, apple_id: str):
    db_user = db.query(User).filter(User.appleId == apple_id).first()
    if db_user:
        return db_user
    else:
        return False


def get_user_by_vk_id(db: Session, vk_id: str):
    db_user = db.query(User).filter(User.vkId == str(vk_id)).first()
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


def create_user_oauth(db: Session, user: user_schema.UserCreateOauth):
    instance = db.query(User).filter(User.email == user.email).first()
    if instance and user.email:
        db_user = db.query(User).filter(User.email == user.email).first()
        db_user.googleId = user.googleId
        db.commit()
        user_dict = db_user.__dict__
        user_dict["role"] = db_user.role.__dict__
        if db_user.photo:
            user_dict["photo"] = db_user.photo.__dict__
        user = user_schema.UserOut(**user_dict)
        return user
    else:
        if user.photo:
            db_photo = Photo(url=user.photo)
            db.add(db_photo)
            db.commit()
            db.refresh(db_photo)
            user.photoId = db_photo.id
        db_user = User(uuid=uuid.uuid4(),
                       email=user.email,
                       name=user.name,
                       surname=user.surname,
                       emailVerified=user.emailVerify,
                       googleId=user.googleId,
                       vkId=user.vkId,
                       appleId=user.appleId,
                       phoneVerified=False,
                       roleId=1,
                       photoId=user.photoId,
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


def check_phone_exist(db: Session, user_data: user_schema.ChangeUser):
    instance = db.query(User).filter(User.phone == user_data.phone).first()
    if instance:
        return False
    return True


def check_email_exist(db: Session, user_data: user_schema.ChangeUser):
    instance = db.query(User).filter(User.email == user_data.email).first()
    print(instance)
    if instance:
        return False
    return True


def change_user_data(db: Session, user: User, user_data: user_schema.ChangeUser):
    if user_data.email:
        user.email = user_data.email
    if user_data.phone:
        user.phone = user_data.phone
    db.commit()
