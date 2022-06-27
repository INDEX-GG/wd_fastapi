from sqlalchemy.orm import Session
from app.schemas import favorites as favorite_schema
from app.db.db_models import Favorites


def create_favorites(db: Session , favorite :favorite_schema.CreateFavorite ):
    check = db.query(Favorites).where(Favorites.userId == favorite.userId, Favorites.objId== favorite.objId).all()
    if check:
        return False


    db_favorite = Favorites (userId=favorite.userId,
                                 objId=favorite.objId)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def read_favorites(user_id : int,db: Session):
    return db.query(Favorites).where(Favorites.userId == user_id).all()



def delete_favorites(db: Session, userId : int , objId : int ):
    delete =  db.query(Favorites).where(Favorites.userId == userId, Favorites.objId == objId).delete(synchronize_session="evaluate")
    db.commit()
    return delete


