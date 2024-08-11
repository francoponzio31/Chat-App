from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
from repositories.sql_connection import BaseModel
from uuid import uuid4


class User:

    def __init__(self, email, username, password, role="user", creation_date=None, picture_id=None, is_verified=False):
        self.email = email
        self.username = username
        self.password = password
        self.role = role
        self.picture_id = picture_id
        self.creation_date = creation_date or datetime.now()
        self.is_verified = is_verified
        self.verification_token = str(uuid4())
        
    def __repr__(self):
        return f"<User {self.email}>"


class UserSQLModel(User, BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(320), unique=True, nullable=False)
    username = Column(String(40), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum("user", "admin", name="user_roles"), nullable=False)
    picture_id = Column(String(36), nullable=True)
    creation_date = Column(DateTime, default=datetime.now, nullable=False)
    is_verified = Column(Boolean, nullable=False)
    verification_token = Column(String(36), nullable=True)


class UserJSONModel(User):

    def __init__(self, id, email, username, password, role="user", creation_date=None, picture_id=None, is_verified=False):
        super().__init__(email, username, password, role, creation_date, picture_id, is_verified)
        self.id = id

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "picture_id": self.picture_id,
            "creation_date": self.creation_date,
            "is_verified": self.is_verified,
            "verification_token": self.verification_token,
        }

    @classmethod
    def from_dict(cls, data:dict):
        return cls(**data)
