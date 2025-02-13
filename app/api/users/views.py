from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from app.api.users import schemas, crud

from app.db.engine import get_db
from app.auth.security import get_current_user, require_role
from app.models.models import User

router = APIRouter()

@router.get("/users/", response_model=list[schemas.User], dependencies=[Depends(require_role("admin"))])
def read_users(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.execute(select(User)).scalars().all()

@router.post("/users/", response_model=schemas.User, dependencies=[Depends(require_role("admin"))])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = User(id=user.id, **user.dict(exclude={"id"}))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=schemas.User)
def read_single_user(user_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user["role"] != "admin" and current_user["email"] != user.email:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return user

@router.delete("/{user_id}", response_model=dict, dependencies=[Depends(require_role("admin"))])
def delete_single_user(user_id: int, db: Session = Depends(get_db)):
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {"message": "User deleted successfully"}

@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user["role"] != "admin" and current_user["email"] != user.email:
        raise HTTPException(status_code=403, detail="Access forbidden")

    update_query = update(User).where(User.id == user_id).values(**user_update.dict(exclude_unset=True))
    db.execute(update_query)
    db.commit()

    updated_user = db.query(User).filter(User.id == user_id).first()
    return updated_user
