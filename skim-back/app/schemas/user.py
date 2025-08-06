from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    auth_key = Column(String, unique=True, nullable=False)
    auth = Column(String, nullable=False)
    hashed_password = Column(String, nullable=True)
