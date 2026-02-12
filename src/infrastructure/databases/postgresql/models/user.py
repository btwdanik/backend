from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from infrastructure.databases.postgresql.session.base import Base

class User(Base):
    __tablename__ = "user"
    #TODO: add new columns for token
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(30))
    email: Mapped[EmailStr] = mapped_column(String(30), unique=True)
    refresh_token: Mapped[str] = mapped_column(String(450))
