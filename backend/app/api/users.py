from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.schemas.user import UserCreate
from backend.app.services.user_service import create_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)