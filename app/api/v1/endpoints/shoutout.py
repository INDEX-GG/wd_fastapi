from fastapi import APIRouter,Depends, Body
from app.api.dependencies import get_db
from sqlalchemy.orm import Session
from app.schemas import user as user_schema, shoutout as shoutout_schema
from app.crud import user as user_crud, shoutout as shoutout_crud

router = APIRouter(prefix="/shoutouts",
                   tags=["shoutout"])


@router.post("", summary="create shoutout") #works correctly
async def create(  create : shoutout_schema.CreateShoutout,
                    current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                    db: Session = Depends(get_db)):
    new_shoutout = shoutout_crud.create_shoutout(db,create,current_user.id)
    return new_shoutout

@router.get("" , summary="get shoutouts me") #works correctly
async def read_shoutouts_me(current_user: user_schema.UserOut = Depends(user_crud.get_current_user),
                            db: Session = Depends(get_db)):
    list_shoutouts_me = shoutout_crud.read_shoutouts(db,current_user.id)
    return list_shoutouts_me





