from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.schemas.user import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user=User(
        full_name=user.full_name,
        phone=user.phone,
        address=user.address,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user