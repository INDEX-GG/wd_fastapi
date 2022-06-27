from sqlalchemy.orm import Session
from app.schemas.shoutout import CreateShoutout,  UpdateShoutout, ShoutoutBase
from app.schemas.user import UserOut
from app.db.db_models import Shoutout


def create_shoutout(db: Session, schoutout : CreateShoutout , cur_user_id : int ):
    check = db.query(Shoutout).where(Shoutout.id_reviewer == cur_user_id, Shoutout.in_regard_to == schoutout.in_regard_to).all()


    if check != []:
        return { "message" : "not created because earlier created"}

    new_shoutout = Shoutout (rating=schoutout.rating,
                            text=schoutout.text,
                            id_reviewer=cur_user_id)
    db.add(new_shoutout)
    db.commit()
    db.refresh(new_shoutout)
    return new_shoutout

def read_shoutouts(db: Session , user_id : int ):
    return db.query(Shoutout).where(Shoutout.id_reviewer == user_id).all()




