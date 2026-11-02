from pydantic import BaseModel,Field
from datetime import datetime



class ExpenseCreate(BaseModel):
    title: str = Field(...,description="The title of the expense", max_length=100)
    description: str = Field(...,   description= "The description of the expense", max_length=200)
    amount: float = Field(..., description="The amount of the expense")
    show: bool =  Field( description="Whether the expense is visible or not", default=True)
   
    

class ExpenseResponse(BaseModel):
    id: int
    title: str
    description: str
    amount: float
    show: bool
    created_at: datetime

    class Config:
        from_attributes = True  # allows pydantic to read SqlAlchemy models and convert them to pydantic models