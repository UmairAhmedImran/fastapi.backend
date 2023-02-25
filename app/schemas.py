from pydantic import BaseModel, EmailStr # use for validating the type of data we need like we use in classes and function ex id: int
from datetime import datetime
from typing import Optional
from pydantic.types import conint
# setting title and content to string if any other data type is given which can not be coverted in string it going to raise error
# class Post(BaseModel): # inherit from BaseModel
#     title: str # define the type of data model
#     content: str
#     published: bool = True # giving it default value true so that if user doesnot provide it so it will not give any error.
#     #rating: Optional[int] = None # default value is none and it is optional data type.

class PostBase(BaseModel):
    title: str 
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class UserOut(BaseModel):
    id: int
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

class PostOut(BaseModel): # because our schema of post was not applicable after joining votes we created this new schema..
    Post: Post
    votes: int
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str



class Userlogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class Token_data(BaseModel):
    id: Optional[str] = None

class vote(BaseModel):
    post_id: int
    dir: conint(le=1)