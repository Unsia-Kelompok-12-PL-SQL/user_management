# file untuk validasi body request

from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    #groups: list = []
    class Config:
        form_attributes = True

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    name: str

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int

class Post(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    class Config:
        form_attributes = True

class SignUp(BaseModel):
    name: str
    email: str
    password: str
    class Config:
        form_attributes = True

class Login(BaseModel):
    email: str
    password: str
    class Config:
        form_attributes = True

class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    class Config:
        form_attributes = True