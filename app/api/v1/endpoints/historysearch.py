from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.dependencies import get_db
from sqlalchemy.orm import Session
from app.schemas import historysearch as history_search_schema, response as response_schema
from app.crud import user as user_crud, historysearch as history_search_crud
from app.schemas import user as user_schema


router = APIRouter(prefix="/history-search",
                   tags=["historySearch"])


@router.post("", summary="Add Record",
             response_model=response_schema.ResponseSuccess,
             status_code=201)
async def add_history_search(req: history_search_schema.CreateHistorySearch,
                             current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                             db: Session = Depends(get_db)):
    history_search_crud.create_history(db=db, id_user=current_user.id, history_search=req)
    return {"message": "success"}


@router.delete("/{record_id}", summary="Delete Record By Id",
               response_model=response_schema.ResponseSuccess)
async def read_history_search(record_id: int,
                              current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                              db: Session = Depends(get_db)):
    deleting = history_search_crud.delete_history(db=db, user_id=current_user.id, record_id=record_id)
    if not deleting:
        raise HTTPException(404)
    return {"message": "success"}


@router.get("", summary="Get All Records",
            response_model=history_search_schema.ListHistory
            )
async def read_history_search(page: int = Query(default=1, ge=1, le=1000),
                              page_limit: int = Query(alias="pageLimit", default=60, ge=1, le=200),
                              current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                              db: Session = Depends(get_db)):
    items = history_search_crud.get_history_search_page_by_page(db=db,
                                                                page=page,
                                                                page_limit=page_limit,
                                                                user_id=current_user.id)
    return items
