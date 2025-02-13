from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.api.users import schemas, crud
from app.api.users.schemas import UserCreate
from app.db.engine import get_db
from app.auth.security import (
    get_password_hash, verify_password, create_access_token,
    get_current_user, hash_password, validate_password_strength
)
from app.models.models import User

router = APIRouter()

@router.post("/register/", response_model=schemas.User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    validate_password_strength(user.password)
    hashed_password = get_password_hash(user.password)

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login/", response_model=schemas.LoginResponse)
async def login(user: schemas.LoginRequest, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db or not verify_password(user.password, user_db.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email, "role": user_db.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserRead)
async def read_me(current_user: schemas.UserRead = Depends(get_current_user)):
    return current_user

@router.post("/reset_password")
async def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, request.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if verify_password(request.new_password, user.hashed_password):
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the old password!"
        )

    user.hashed_password = hash_password(request.new_password)
    db.commit()
    return {"detail": "Password updated"}
