from backend.app.database.base import Base
from backend.app.database.connection import engine

#import all models
from backend.app.models.user import User

print("Creating database table...")

Base.metadata.create_all(bind=engine)

print("Done!")