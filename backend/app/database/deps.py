from sqlalchemy.orm import Session

from backend.app.database.connection import SessionLocal

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()