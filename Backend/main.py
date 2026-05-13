from fastapi import FastAPI,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,EmailStr,field_validator
from db_model import SessionLocal,base,engine,User
from sqlalchemy.orm import Session
import re

app=FastAPI()
origins=[
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
def dbconfig():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

class userValid(BaseModel):
    email:EmailStr
    password:str

    @field_validator("password")
    @classmethod
    def passwordValidate(cls,val:str):
        if len(val)<8:
            raise HTTPException(status_code=422,detail="Password is must be more then 8 character")
        elif not re.search(r"[A-Z]",val):
            raise HTTPException(status_code=422,detail="atleast one capital letter must be there")
        elif not re.search(r"[a-z]",val):
            raise HTTPException(status_code=422,detail="atleast one small letter must be there")
        elif not re.search(r"[0-9]",val):
            raise HTTPException(status_code=422,detail="password must contains a number")
        elif not re.search(r"[@#$%^&]",val):
            raise HTTPException(status_code=422,detail="password must contains a speacial character")
        else:
            return val


@app.post("/userdata")
def newuser(userModel:userValid,db:Session=Depends(dbconfig)):
    user=db.query(User).filter(userModel.email==User.email).first()
    if user:
        raise HTTPException(status_code=409,detail="User already exist")
    model=User(
        email=userModel.email,
        password=userModel.password
    )
    db.add(model)
    db.commit()
    db.refresh(model)


base.metadata.create_all(bind=engine)