from fastapi import FastAPI
from database import Base,engine
import models
from router import auth
app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(auth.router)

@app.get("/")
def root():
    return {
        "message": "Welcome back to Auth Api"
    }


@app.get("/home")
def home():
    return {
        "message": "Welcome home"
    }


@app.get("/about")
def about():
    return {
        "name": "Abhishek",
        "address": "Delhi",
        "pin": "12"
    }
