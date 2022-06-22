from fastapi import APIRouter,Depends, Body
from app.crud import user as user_crud, favorites as favorites_crud
from app.schemas import favorites as favarites_schema, user as user_schema, post as PostSchema
from app.api.dependencies import get_db

from sqlalchemy.orm import Session

router = APIRouter(prefix="/favorites",
                   tags=["favorites"])

#рассмотреть если избранное пустое, вернуть пустой массив, иначе вернуть массив избранного

@router.delete("")
async def delete_favorite(obj : PostSchema.PostOut,
                          current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                          db: Session = Depends(get_db)):
    return favorites_crud.delete_favorites(db,
                                           current_user.id,
                                           obj.id)

@router.get("")
async def get_favorites( current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                         db: Session = Depends(get_db)):
    list_favorites = favorites_crud.read_favorites(current_user.id,
                                                   db)
    return list_favorites

@router.post("",summary="Create Favorite")
async def create_favorite(obj : PostSchema.PostOut,
                          current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                          db: Session = Depends(get_db)):

    new_favorite = favorites_crud.create_favorites(db,
                                                 favarites_schema.CreateFavorite(userId=current_user.id,
                                                                                 objId=obj.id))

    return {"message" : "add" if new_favorite != False else "previously added" ,
            "new_favorite" : new_favorite}
