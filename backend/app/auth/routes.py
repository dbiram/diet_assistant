from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import models, schemas, auth_utils

router = APIRouter(prefix="/auth")

@router.post("/register", response_model=schemas.Token)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter_by(username=user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = auth_utils.hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = auth_utils.create_access_token({"sub": user.username})
    return {"access_token": token}

@router.post("/login", response_model=schemas.Token)
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter_by(username=username).first()
    if not db_user or not auth_utils.verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth_utils.create_access_token({"sub": username})
    return {"access_token": token}
