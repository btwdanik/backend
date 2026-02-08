from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from infrastructure.databases.postgresql.session.base import Base

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    category: Mapped[str] = mapped_column(String(100))
    count: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
