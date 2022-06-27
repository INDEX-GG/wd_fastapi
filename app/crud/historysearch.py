from sqlalchemy.orm import Session
from app.db.db_models import HistorySearch
from app.schemas import historysearch


def create_history(db: Session , id_user: int  ,historysearch : historysearch.CreateHistorySeqrch ):
    count = db.query(HistorySearch).where(HistorySearch.userId == id_user).count()

    if count > 4:
        dele =db.query(HistorySearch).where(HistorySearch.userId == id_user).first()
        db.delete(dele)
        db.commit()


    new_histor = HistorySearch(userId=id_user,
                               searchQuery=historysearch.searchQuery,
                               flagPrice=historysearch.flagPrice,
                               price=historysearch.price)
    db.add(new_histor)
    db.commit()
    db.refresh(new_histor)
    return new_histor


def read_history(db: Session , user_id : int):
    return db.query(HistorySearch).where(HistorySearch.userId == user_id).all()

def delete_history(db: Session):
    return 0