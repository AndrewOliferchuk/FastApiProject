from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session, joinedload

from app.api.skills import schemas
from app.api.skills import crud
from app.db.engine import get_db
from app.models.models import Skill

router = APIRouter()

@router.get("/skills/")
def get_skills(db: Session = Depends(get_db)):
    query = select(Skill).options(joinedload(Skill.user))
    result = db.execute(query)
    return result.scalars().all()


@router.get("/skills/{skill_id}")
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    return crud.get_skill_by_id(db=db, skill_id=skill_id)


@router.post("/skills/")
def create_skill(skill: schemas.SkillCreate, db: Session = Depends(get_db)):
    new_skill = Skill(
        id=skill.id,
        skill_name=skill.skill_name,
        proficiency=skill.proficiency,
        user_id=skill.user_id
    )
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill


@router.delete("/skills/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    db.execute(delete(Skill).where(Skill.id == skill_id))
    db.commit()
    return {"message": "Skill deleted successfully"}


@router.patch("/skills/{skill_id}")
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
