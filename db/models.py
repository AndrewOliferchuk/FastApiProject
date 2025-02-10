from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import  mapped_column, Mapped, relationship, declarative_base

Base = declarative_base()


class Hobby(Base):
    __tablename__ = 'hobbies'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    category: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(911))

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates="hobbies")

class Skill(Base):
    __tablename__ = 'skills'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=False)
    skill_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    proficiency: Mapped[Optional[str]] = mapped_column(String(100))

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped["User"] = relationship(back_populates="skills")


class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[Optional[str]] = mapped_column(String(100))
    city: Mapped[Optional[str]] = mapped_column(String(40))
    country: Mapped[Optional[str]] = mapped_column(String(40))

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates="addresses")

class Education(Base):
    __tablename__ = 'educations'

    id: Mapped[int] = mapped_column(primary_key=True)
    degree: Mapped[Optional[str]] = mapped_column(String(100))
    school_name: Mapped[Optional[str]] = mapped_column(String(100))
    university_name: Mapped[Optional[str]] = mapped_column(String(100))

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates="educations")


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    review_text: Mapped[str] = mapped_column(String(911), nullable=False)
    rating: Mapped[Optional[int]] = mapped_column(Integer)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates="reviews")

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), index=True)
    last_name: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    role: Mapped[str] = mapped_column(String(100), default="user")
    hashed_password: Mapped[str] = mapped_column(String(500))


    hobbies: Mapped[List["Hobby"]] = relationship(back_populates="user", cascade='all, delete-orphan')
    skills: Mapped[List["Skill"]] = relationship(back_populates="user", cascade='all, delete-orphan')
    addresses: Mapped[List["Address"]] = relationship(back_populates="user", cascade='all, delete-orphan')
    educations: Mapped[List["Education"]] = relationship(back_populates="user", cascade='all, delete-orphan')
    reviews: Mapped[List["Review"]] = relationship(back_populates="user", cascade='all, delete-orphan')