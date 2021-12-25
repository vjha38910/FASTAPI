from os import access
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app import oauth2, utils
from .. import  schemas, models
from..database import  get_db

router = APIRouter(
   # prefix="/",
    tags=['Authentication']
)


@router.post("/login",response_model=schemas.Token)
#def login(user_credetials: schemas.UserLogin , db:Session = Depends(get_db)):
def login(user_credetials: OAuth2PasswordRequestForm= Depends() , db:Session = Depends(get_db)):
 
    # oauth will always have data in this format 
    # {
    #     "username" : "email in our case",
    #     "password" : "password"
    # }
    #user = db.query(models.User).filter(models.User.email == user_credetials.email).first()
    user = db.query(models.User).filter(models.User.email == user_credetials.username).first()


    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Invalid credentials")

    if not utils.verify(user_credetials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    access_token = oauth2.create_access_token(data= {"user_id": user.id, "name": user.name})
   
    return {"access_token": access_token, "token_type":"bearer"}

