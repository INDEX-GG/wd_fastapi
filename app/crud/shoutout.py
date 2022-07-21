from sqlalchemy.orm import Session, joinedload
from typing import List
import datetime
from app.schemas import shoutout as shoutout_schema
from app.db.db_models import Shoutout, User


def create_shoutout(db: Session, shoutout: shoutout_schema.CreateShoutout, user_id: int):
    db_shoutout = Shoutout(
        userId=user_id,
        text=shoutout.text,
        createdAt=datetime.datetime.utcnow(),
        rating=shoutout.rating
    )
    db.add(db_shoutout)
    db.commit()
    return True


def read_user_shoutouts(db: Session, user_id: int, page_limit: int, page: int):
    offset = (page - 1) * page_limit
    query = db.query(Shoutout)\
        .options(joinedload(Shoutout.user)) \
        .where(Shoutout.userId == user_id)\
        .order_by(Shoutout.id.desc())
    shoutouts = query.offset(offset).limit(page_limit).all()
    return shoutouts


def read_all_shoutouts(db: Session, page_limit: int, page: int):
    offset = (page - 1) * page_limit
    query = db.query(Shoutout)\
        .options(joinedload(Shoutout.user)) \
        .order_by(Shoutout.id.desc())
    shoutouts = query.offset(offset).limit(page_limit).all()
    return shoutouts


def get_shoutout_out(db_shoutout: Shoutout):
    shoutout_dict = db_shoutout.__dict__
    shoutout_dict["user"] = db_shoutout.user.__dict__
    shoutout_out = shoutout_schema.ShoutoutOut(**shoutout_dict)
    print(shoutout_out)
    return shoutout_out


def get_shoutouts_out(db_shoutouts: List[Shoutout]):
    shoutouts_out = []
    for db_shoutout in db_shoutouts:
        shoutouts_out.append(get_shoutout_out(db_shoutout))
    return shoutouts_out
