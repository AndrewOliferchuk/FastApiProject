from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session, joinedload
from starlette import status
import crud
import schemas
from db.engine import get_db
from security import get_password_hash, verify_password, create_access_token, \
    get_current_user, hash_password, validate_password_strength, require_role
from db.models import User, Skill
from schemas import UserCreate

app = FastAPI()

@app.get("/")
def read_root() -> dict:
    return {"message": "qwe, FastAPI!"}


@app.post("/register/", response_model=schemas.User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    exiting_user = db.query(User).filter(User.email == user.email).first()
    if exiting_user:
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


@app.post("/login/", response_model= schemas.LoginResponse)
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


@app.get("/me", response_model=schemas.UserRead)
async def read_me(current_user: schemas.UserRead = Depends(get_current_user)):
    return current_user

@app.post("/reset_password")
async def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, request.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if verify_password(request.new_password, user.hashed_password):
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the old password!")

    user.hashed_password = hash_password(request.new_password)
    db.commit()
    return {"detail": "Password updated"}


@app.get("/users/", response_model=list[schemas.User], dependencies=[Depends(require_role("admin"))])
def read_users(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.execute(select(User)).scalars().all()

@app.post("/users/", response_model=schemas.User, dependencies=[Depends(require_role("admin"))])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = User(id=user.id, **user.dict(exclude={id}))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=schemas.User)
def read_single_user(
        user_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user["role"] != "admin" and current_user["email"] != user.email:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return user

@app.delete(
    "/users/{user_id}", response_model=schemas.User, dependencies=[Depends(require_role("admin"))])
def delete_single_user(user_id: int, db: Session = Depends(get_db)):
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {"message": "User deleted successfully"}


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(
        user_id: int, user_update: schemas.UserUpdate, current_user: dict = Depends(get_current_user),  db: Session = Depends(get_db)):
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






@app.get("/skills/")
def get_skills(db: Session = Depends(get_db)):
    query = select(Skill).options(joinedload(Skill.user))
    result = db.execute(query)

    skills = result.scalars().all()
    return skills

@app.get("/skills/{skill_id}")
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    return crud.get_skill_by_id(db=db, skill_id=skill_id)

@app.post("/skills/")
def create_skill(skill: schemas.SkillCreate, db: Session = Depends(get_db)):
    new_skill = Skill(
        id=skill.id, skill_name=skill.skill_name, proficiency=skill.proficiency, user_id=skill.user_id)
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill

@app.delete("/skills/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    db.execute(delete(Skill).where(Skill.id == skill_id))
    db.commit()
    return {"message": "Skill deleted successfully"}


@app.patch("/skills/{skill_id}")
def update_skill(skill_id: int, skill_update: schemas.SkillUpdate, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found for this user")
    db.execute(
        update(Skill)
        .where(Skill.id == skill_id)
        .values(skill_update.dict(exclude_unset=True))
    )
    db.commit()
    updated_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    return updated_skill



