from .connection import engine
from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print(result.fetchone())
        print("Database connected successfully!")
except Exception as e:
    print("Connection failed!")
    print(e)