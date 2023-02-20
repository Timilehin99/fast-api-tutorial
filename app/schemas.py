from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    published : bool = True

class Vote(BaseModel):
    id: int
    direction : int 


class CreateUser(BaseModel):
    email: EmailStr
    password: str

class CreatePost(Post):
    pass

class UpdatePost(Post):
    published : bool

class UserResponse(BaseModel):
    email: EmailStr
    created_at: datetime


    class Config:
        orm_mode = True
        
class PostResponse(BaseModel):
    title: str
    content: str
    published: str
    user_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post : PostResponse
    votes : int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] =None
