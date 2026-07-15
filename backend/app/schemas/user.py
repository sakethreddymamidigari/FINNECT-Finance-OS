from pydantic import BaseModel

class UserCreate(BaseModel):
    full_name:str
    phone:str
    address:str