from sqlalchemy.orm import Session
from sqlalchemy.orm.strategy_options import joinedload
from app.models import models
from app.api.skills import schemas

def get_all_skills(db: Session):
    return db.query(models.Skill).options(joinedload(models.Skill.user)).all()

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
