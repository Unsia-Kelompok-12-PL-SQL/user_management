from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI() 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""" ---on progress---
@app.middleware("http")
async def check_authorize(request: Request, call_next, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    token = auth_header[7:]
    db_user = crud.get_current_user(db, token=token)
    response = await call_next(request)
    print("inside middleware")
    return response
"""

@app.get("/")
async def root():
    return {"message": "Hello World"}

"""@app.post("/api/v1/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(db=db, user=user)"""

@app.post("/api/v1/groups/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    db_group = crud.get_group_by_name(db, name=group.name)
    if db_group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Group already exists")
    return crud.create_group(db=db, group=group)

@app.post("/api/v1/token")
def create_token(email: int, db: Session = Depends(get_db)):
    generated_token = crud.create_token({"sub": email})
    return generated_token

@app.post("/api/v1/login")
def login(user: schemas.Login, db: Session = Depends(get_db)):
    return crud.login(db=db, user=user)

@app.post("/api/v1/sign_up")
def sign_up(user: schemas.UserCreate, db: Session = Depends(get_db)):
    verify_email = crud.get_user_by_email(db, email=user.email)
    if verify_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.sign_up(db=db, user=user)

@app.put("/api/v1/users/{user_id}")
def update_user(user_id: int, user: schemas.UpdateUser, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return crud.update_user(db=db, user=user, user_id=user_id)

@app.delete("/api/v1/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return crud.delete_user(db=db, user_id=user_id)

@app.get("/api/v1/posts/", response_model=schemas.Post)
def get_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db=db)

@app.post("/api/v1/posts/")
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post, user_id=1)

@app.put("/api/v1/posts/{post_id}")
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return crud.update_post(db=db, post=post, post_id=post_id)

@app.delete("/api/v1/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return crud.delete_post(db=db, post_id=post_id)
