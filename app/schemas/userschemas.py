from datetime import datetime

from pydantic import BaseModel,EmailStr,ConfigDict

#schemas fro user data validation
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserRessponse(BaseModel):
    #model_config=ConfigDict(from_attributes=True)
    id:int
    username:str
    email:str
    created_at:datetime
    class Config:from_attributes=True# allows pydantic to read SqlAlchemy models and convert them to pydantic models    
