from fastapi import APIRouter,Depends
from app.api.dependencies import get_db
from sqlalchemy.orm import Session
from app.schemas.historysearch import CreateHistorySeqrch
from app.crud import user as user_crud, historysearch as history_search_crud
from app.schemas import  user as user_schema


router = APIRouter(prefix="/hs",
                   tags=["historySearch"])

@router.post("", summary="add to list")
async def add_history_serach( req : CreateHistorySeqrch,
                              current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                              db: Session = Depends(get_db)):
    return history_search_crud.create_history(db, current_user.id , req )

@router.get("", summary="read list historySearch")
async def read_histoury_search(current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                              db: Session = Depends(get_db)):
    list_hislory = history_search_crud.read_history(db, current_user.id)
    return list_hislory

