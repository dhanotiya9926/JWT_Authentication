from fastapi import APIRouter,Depends,HTTPException,status
from schemas import User_create,User_response,User_login
from database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from models import User
from sqlalchemy import select
from security import hash_password,verify_password,create_access_token

router=APIRouter()
my_auth=OAuth2PasswordBearer(tokenUrl="/login")

@router.post("/register",response_model=User_response)

def register(user_data:User_create, db:Session=Depends(get_db)):
    
    user_existing=db.execute(select(User).where(User.email==user_data.email)).scalar_one_or_none()

    if user_existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User Already exists with this email"
        )
    hashed_password=hash_password(user_data.password)
    user=User(
        full_name=user_data.full_name,
        email=user_data.email,
        hash_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
@router.post("/login")
def login(user:User_login,db:Session=Depends(get_db)):

    db_user=db.execute(select(User).where(User.email==user.email)).scalar_one_or_none()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not exists"
        )

    is_valid=verify_password(user.password,db_user.hash_password)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    data={"sub":db_user.email}
    access_token=create_access_token(data)

    return {
        "message":"Token generated successfully",
        "access token":access_token
    }
# @router.get("/profile")
# def profile(token:str=Depends(my_auth))