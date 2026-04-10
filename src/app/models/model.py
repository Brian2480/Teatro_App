from __future__ import annotations
from dataclasses import dataclass
from flask_login import UserMixin
from typing import List
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from src.app.extension import db, login_manager
from src.app.database.base import Base


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(Base, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), unique=False, nullable=False, init=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Registro(Base):
    __tablename__ = 'register'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    student: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    campus: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    group: Mapped[str] = mapped_column(String(5), unique=False, nullable=False)
    qr_url: Mapped[str] = mapped_column(String(500), unique=True, nullable=True )
    qr_public_id: Mapped[str] = mapped_column(String(500), unique=True, nullable=True )


class Plantel(Base):
    __tablename__ = 'planteles'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    plantel: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    grupos: Mapped[List[Grupo]] = relationship(back_populates='plantel', cascade="all, delete-orphan", init=False)


class Grupo(Base):
    __tablename__ = 'grupos'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name_group: Mapped[str] = mapped_column(String(50), nullable=False)

    #Relacion y llave Foranea
    plantel_id: Mapped[int] = mapped_column(ForeignKey('planteles.id'))
    plantel: Mapped[Plantel] = relationship(back_populates='grupos', init=False)


class File(Base):
    __tablename__ = 'files'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    file_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    pdf_url: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    pdf_public_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)