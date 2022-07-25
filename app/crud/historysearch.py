from sqlalchemy.orm import Session
import datetime
from app.db.db_models import HistorySearch
from app.schemas import historysearch as history_search_schema


def create_history(db: Session, id_user: int, history_search: history_search_schema.CreateHistorySearch):
    db_history_record = HistorySearch(userId=id_user,
                                      searchQuery=history_search.searchQuery,
                                      withContractPrice=history_search.withContractPrice,
                                      price=history_search.price,
                                      createdAt=datetime.datetime.utcnow())
    db.add(db_history_record)
    db.commit()
    return True


def delete_history(db: Session, user_id: int, record_id: int):
    db_record = db.query(HistorySearch).where(HistorySearch.userId == user_id, HistorySearch.id == record_id).first()
    if db_record is None:
        return False
    db.delete(db_record)
    db.commit()
    return True


def get_history_search_page_by_page(db: Session, user_id: int, page: int, page_limit: int):
    offset = (page - 1) * page_limit
    query = db.query(HistorySearch).where(HistorySearch.userId == user_id).order_by(HistorySearch.id.desc())
    posts_count = None
    if page == 1:
        posts_count = query.count()
    db_history_search = query.offset(offset).limit(page_limit).all()
    return history_search_schema.ListHistory(searchHistory=db_history_search, searchHistoryCount=posts_count)
