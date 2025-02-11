from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class UserCreate(UserBase):
    password: str
    role: str

    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True

class UserRead(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True

class UserBlock(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


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

    class Config:
        from_attributes = True