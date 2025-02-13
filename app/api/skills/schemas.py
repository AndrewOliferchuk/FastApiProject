from typing import Optional

from pydantic import BaseModel

from app.models.models import User


class SkillBase(BaseModel):
    skill_name: str
    proficiency: str
    user_id: int

class SkillCreate(SkillBase):
    id: int

class SkillUpdate(BaseModel):
    skill_name: Optional[str] = None
    proficiency: Optional[str] = None
    user_id: Optional[int] = None

class Skill(SkillBase):
    id: int
    user: Optional[User]

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }