from sqlalchemy.orm import Session
from sqlalchemy.orm.strategy_options import joinedload

from db import models
import schemas

def get_all_user(db: Session):
    return  db.query(models.User).all()

def get_user_by_email(db: Session, email: str):
    return (
        db.query(models.User).filter(models.User.email == email).first()
    )

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_skill(db: Session):
    return db.query(models.Skill).options(joinedload(models.Skill.user)).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_skill_by_id(db: Session, skill_id: int):
    return db.query(models.Skill).filter(models.Skill.id == skill_id).first()

def create_skill(db: Session, skill: schemas.SkillCreate):
    skill = models.Skill(
        skill_name=skill.skill_name,
        proficiency=skill.proficiency,
        user_id=skill.user_id
    )
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill
