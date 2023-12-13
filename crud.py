# melakukan operasi CRUD ke database dan handle logic dari aplikasi kita.

from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from .helper import hash_password, verify_password, create_token



def sign_up(user: schemas.UserCreate, db: Session):
    hashed_password = hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"data":{"name": db_user.name, "email": db_user.email},
            "message": "User created" }

def login(user: schemas.Login, db: Session):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=404, detail="Incorrect password")
    return {"message": "Login successful",
            "data": {"token": create_token({"sub": db_user.email})}
    }



def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id ).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

""" ---on progress---
def get_current_user(db: Session, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        print("payload")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db_user = db.query(models.User).where(User.c.id == user_id)
    if db_user is None:
        raise credentials_exception
    return db_user
"""


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_group_by_name(db: Session, name: str):
    return db.query(models.Group).filter(models.Group.name == name).first()

def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(title=post.title, content=post.content, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_user(db: Session, user_id: int, user: schemas.UpdateUser):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if user.name:
        db_user.name = user.name
    if user.email:
        db_user.email = user.email
    if user.password:
        db_user.password = hash_password(user.password)
    db.commit()
    db.refresh(db_user)
    return {"message": "User updated"}

def delete_user(db: Session, user_id= int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}