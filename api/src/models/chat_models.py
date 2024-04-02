from sqlalchemy import Column, Integer, String, DateTime, Boolean
from repositories.sql_connection import BaseModel
from datetime import datetime


class Chat:

    def __init__(self, is_group, group_name=None, creation_date=None):
        self.is_group = is_group
        self.group_name = group_name
        self.creation_date = creation_date or datetime.now()

    def __repr__(self):
        return f"<Chat {self.id}>"


class ChatSQLModel(Chat, BaseModel):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_group = Column(Boolean, nullable=False)
    group_name = Column(String(50), nullable=True)
    creation_date = Column(DateTime, default=datetime.now, nullable=False)


class ChatJSONModel(Chat):

    def __init__(self, id, is_group, group_name=None, creation_date=None):
        super().__init__(is_group, group_name, creation_date)
        self.id = id

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "is_group": self.is_group,
            "group_name": self.group_name,
            "creation_date": self.creation_date
        }

    @classmethod
    def from_dict(cls, data:dict):
        return cls(**data)
