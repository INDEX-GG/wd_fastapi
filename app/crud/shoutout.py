from sqlalchemy.orm import Session
import datetime
from app.schemas import shoutout as shoutout_schema
from app.db.db_models import Shoutout


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
    query = db.query(Shoutout).where(Shoutout.userId == user_id).order_by(Shoutout.id.desc())
    shoutouts = query.offset(offset).limit(page_limit).all()
    return [x.__dict__ for x in shoutouts]


def read_all_shoutouts(db: Session, page_limit: int, page: int):
    offset = (page - 1) * page_limit
    query = db.query(Shoutout).order_by(Shoutout.id.desc())
    shoutouts = query.offset(offset).limit(page_limit).all()
    return [x.__dict__ for x in shoutouts]
