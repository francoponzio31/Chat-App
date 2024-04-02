from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from repositories.sql_connection import BaseModel


class User:

    def __init__(self, email, username, role, last_connection=None, creation_date=None, password=None, picture_id=None):
        self.email = email
        self.username = username
        self.password = password
        self.role = role
        self.picture_id = picture_id
        self.creation_date = creation_date or datetime.now()
        self.last_connection = last_connection

    def __repr__(self):
        return f"<User {self.email}>"


class UserSQLModel(User, BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(320), unique=True, nullable=False)
    username = Column(String(40), nullable=False)
    password = Column(String(45), nullable=True)
    role = Column(Enum("user", "admin", name="user_roles"), nullable=False)
    picture_id = Column(String(36), nullable=True)
    creation_date = Column(DateTime, default=datetime.now, nullable=False)
    last_connection = Column(DateTime, nullable=True)


class UserJSONModel(User):

    def __init__(self, id, email, username, role, last_connection=None, creation_date=None, password=None, picture_id=None):
        super().__init__(email, username, role, last_connection, creation_date, password, picture_id)
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
            "last_connection": self.last_connection
        }

    @classmethod
    def from_dict(cls, data:dict):
        return cls(**data)
