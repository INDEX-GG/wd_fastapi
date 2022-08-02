from fastapi import APIRouter, Depends, Query
from typing import List
from app.crud import user as user_crud, favorites as favorites_crud
from app.schemas import favorites as favorites_schema, user as user_schema, post as post_schema
from app.api.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/favorites",
                   tags=["favorites"])


@router.delete("")
async def delete_favorite(obj: post_schema.PostOut,
                          current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                          db: Session = Depends(get_db)):
    return favorites_crud.delete_favorites(db,
                                           current_user.id,
                                           obj.id)


@router.get("", summary="Get favorites posts page by page", tags=[],
            response_model=post_schema.FavoritePosts
            )
async def get_favorites(
        current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
        page: int = Query(default=1, ge=1, le=1000),
        page_limit: int = Query(alias="pageLimit", default=60, ge=1, le=200),
        db: Session = Depends(get_db)):

    list_favorites = favorites_crud.read_favorites(db=db, user_id=current_user.id, page_limit=page_limit, page=page)
    return list_favorites


@router.post("", summary="Create Favorite")
async def create_favorite(obj: post_schema.PostOut,
                          current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                          db: Session = Depends(get_db)):

    new_favorite = favorites_crud.create_favorites(db,
                                                   favorites_schema.CreateFavorite(userId=current_user.id,
                                                                                   objId=obj.id))

    return {"message": "add" if new_favorite != False else "previously added",
            "new_favorite": new_favorite}
