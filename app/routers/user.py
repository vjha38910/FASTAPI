from fastapi import FastAPI, Response, responses, status, HTTPException, Depends, APIRouter
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from typing import  List
from sqlalchemy.sql.functions import user
from sqlalchemy.orm import Session#, session
from..import models, schemas, utils
from..database import  get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db:Session = Depends(get_db)):

    # HASH THE PASSWORD- user.password
    user.password= utils.hash(user.password)
    print(user)
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    
    return user
