from fastapi import FastAPI,Depends,HTTPException,status,APIRouter
from app.core.db import get_db
from app.models.users import User
from app.schemas.apiresponse import APIResponse
from app.schemas.userschemas import UserCreate, UserRessponse
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users")


#create user
@router.post("/",response_model=APIResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    #check if user with the same email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    #create new user
    user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )


    db.add(user)
    db.commit()
    db.refresh(user)
    return APIResponse(status="success", message="User created successfully",
                        data={"user":UserRessponse.model_validate(user)})

#get all users
@router.get("/",response_model=APIResponse)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return APIResponse(status="success", message="Users retrieved successfully",
                        data={"users":[UserRessponse.model_validate(user) for user in users]}) 

#get user by id
@router.get("/{user_id}",response_model=APIResponse)

def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return APIResponse(status="success", message="User retrieved successfully",
                        data={"user":UserRessponse.model_validate(user)})   
#Update user by id
@router.put("/{user_id}",response_model=APIResponse)
def update_user(user_id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    #check if user with the same email already exists
    existing_user = db.query(User).filter(User.email == user_update.email).first()
    if existing_user and existing_user.id != user_id:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    user.username = user_update.username
    user.email = user_update.email
    user.password = user_update.password

    db.commit()
    db.refresh(user)
    return APIResponse(status="success", message="User updated successfully",
                        data={"user":UserRessponse.model_validate(user)})

#Delete user by id
@router.delete("/{user_id}",response_model=APIResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return APIResponse(status="success", message="User deleted successfully")

#search user by username
@router.get("/search/{username}",response_model=APIResponse)
def search_users(username: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.username.ilike(f"%{username}%")).all()
    return APIResponse(status="success", message="Users retrieved successfully",
                        data={"users":[UserRessponse.model_validate(user) for user in users]})  