from sqlalchemy.orm import Session
from sqlalchemy import delete
from app.schemas import favorites
from app.db.db_models import Favorites as DbFavorites


def create_favorites(db: Session , favorite: favorites.Favorite ):
    db_favorite = DbFavorites(userId=favorite.userId,
                            objId=favorite.objId)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def read_favorites(db: Session, user_id : int):
    db_favorites = db.query(DbFavorites).filter(DbFavorites.userId == user_id).all()
    return db_favorites


def delete_favorites(db: Session, favorite: favorites.Favorite ):
    stmt = (
        delete(DbFavorites).
        where(DbFavorites.userId == favorite.userId,  DbFavorites.objId == favorite.objId )
    )
    return stmt;

