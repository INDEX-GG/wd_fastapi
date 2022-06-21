from fastapi import APIRouter,Depends
from app.crud import user as user_crud
from app.schemas import favorites, user as user_schema
from app.api.dependencies import get_db

from sqlalchemy.orm import Session

router = APIRouter(prefix="/favorites",
                   tags=["favorites"])

#рассмотреть если избранное пустое, вернуть пустой массив, иначе вернуть массив избранного

@router.get("")
async def get_favorites():
    return 0


@router.post("",summary="Create Favorite",
             response_model=favorites.Favorite)
async def create_favorite(current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                          db: Session = Depends(get_db)):

    return 0
