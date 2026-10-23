from passlib.context import CryptContext
from datetime import datetime,timezone,timedelta
from jose import jwt
from fastapi import Depends,HTTPException
from router.auth import my_auth
from database import get_db
from sqlalchemy.orm import sessionmaker,Session
from models import User
from sqlalchemy import select


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
SECRETKEY="YOUR SECRET KEY"
ALGORITHM="HS256"

def hash_password(plain_password):
    return pwd_context.hash(plain_password)

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=30)

    to_encode.update({
        "exp":expire
    })

    token=jwt.encode(to_encode,SECRETKEY,algorithm=ALGORITHM)

    return token
def get_access_token(token:str=Depends(my_auth),db:Session=Depends(get_db)):

    try:
        payload=jwt.decode(token,SECRETKEY,algorithms=[ALGORITHM])

        email=payload.get("sub")

        if not email:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        user=db.execute(select(User).where(User.email==email)).scalar_one_or_none()

        return user
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid token or expired token"
        )
    


