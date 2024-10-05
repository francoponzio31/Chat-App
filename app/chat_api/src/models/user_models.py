from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
from repositories.sql_connection import BaseModel
from uuid import uuid4


class UserModel(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(320), unique=True, nullable=False)
    username = Column(String(40), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum("user", "admin", name="user_roles"), nullable=False, default="user")
    picture_id = Column(String(36), nullable=True)
    creation_date = Column(DateTime, default=datetime.now, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    verification_token = Column(String(36), nullable=False, default=str(uuid4()))

    def __str__(self) -> str:
        return "User"