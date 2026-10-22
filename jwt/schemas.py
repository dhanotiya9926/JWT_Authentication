from pydantic import BaseModel,EmailStr,ConfigDict

class User_create(BaseModel):
    full_name:str
    email:EmailStr
    password:str

class User_response(BaseModel):
    full_name:str
    email:str

model_config=ConfigDict(from_attributes=True)

class User_login(BaseModel):
    email:EmailStr
    password:str