import sqlalchemy

from sqlalchemy import String, Integer, Boolean, func, ForeignKey, ARRAY
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, relationship
from typing import Optional, List
from datetime import datetime


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False, onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class User(Base):
    chat_id: Mapped[int] = mapped_column(Integer, unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    profile: Mapped['Profile'] = relationship(
        'Profile',
        back_populates='user',
        uselist=False,
        lazy='joined'
    )
    websites: Mapped['Website'] = relationship(
        'Website',
        back_populates='user',
        cascade='all, delete-orphan',
    )

class Profile(Base):
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    first_name: Mapped[Optional[str]] = mapped_column(String)
    last_name: Mapped[Optional[str]] = mapped_column(String)
    user: Mapped['User'] = relationship(
        'User',
        back_populates='profile',
        uselist=False,
    )


class Website(Base):
    domain: Mapped[Optional[str]] = mapped_column(String)
    user: Mapped['User'] = relationship(
        'User',
        back_populates='websites',
    )
    forms: Mapped['Form'] = relationship(
        'Form',
        back_populates='website',
        cascade='all, delete-orphan',
    )

class Form(Base):
    name: Mapped[str] = mapped_column(String, nullable=False)
    website: Mapped['Website'] = relationship(
        'Website',
        back_populates='forms',
    )
