from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint
from sqlalchemy.sql.elements import Null

# title str , content str, categry, Bool publish or save content
class PostBase(BaseModel): # BaseModelcomes from pydantic library
  
    title: str
    content: str
    published: bool = True
      # rating: Optional[int] = None

# class post is referenced in path operations 

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(Post):
    #Post:Post
    votes: int = 0

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

   

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
   # name: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)