from passlib.context import CryptContext
from datetime import datetime,timezone,timedelta
from jose import jwt

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