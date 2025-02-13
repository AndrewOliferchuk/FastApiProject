from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }

class UserCreate(UserBase):
    password: str
    role: str

    class Config:
        model_config = {
            "from_attributes": True,
            "arbitrary_types_allowed": True
        }

class User(UserBase):
    id: int
    role: str

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }

class UserRead(UserBase):
    id: int
    role: str

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }

class UserBlock(UserBase):
    id: int
    is_active: bool

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str
