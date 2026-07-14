from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
class Post(PostBase): #response you send back to user
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

class Config:
    orm_mode = True
    
class PostOut(BaseModel):
    Post: Post
    votes: int
    
class PostUpdate(PostBase):
    pass

class UserCreate(BaseModel):
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
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore #ge = greater than or equal to 0, le = less than or equal to 1    
    
