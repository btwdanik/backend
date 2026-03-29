from pydantic import EmailStr
from sqlalchemy import String, LargeBinary
from sqlalchemy.orm import mapped_column, Mapped

from src.infrastructure.databases.postgresql.session.base import Base

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary(128))
    email: Mapped[EmailStr] = mapped_column(String(30), unique=True)
    refresh_token: Mapped[str] = mapped_column(String(450))
