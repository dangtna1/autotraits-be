from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta

from app.schemas.auth import UserCreate, UserInDB, Token
from app.db.models.plant import User, Breeder
from app.dependencies import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
router = APIRouter()


@router.post("/signup", response_model=UserInDB)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # create breeder if provided
    if user.breeder_name:
        breeder = db.query(Breeder).filter(Breeder.name == user.breeder_name).first()
        if not breeder:
            breeder = Breeder(name=user.breeder_name)
            db.add(breeder)
            db.commit()
            db.refresh(breeder)
    else:
        raise HTTPException(status_code=400, detail="Breeder name required")

    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name,
        role="admin",
        breeder_id=breeder.id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {"user_id": user.id, "breeder_id": user.breeder_id, "role": user.role},
        timedelta(minutes=60 * 24),
    )
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    data = decode_access_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
