from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from repositories.sql_connection import BaseModel
from datetime import datetime


class ChatMember:

    def __init__(self, chat_id, user_id, joined_date=None):
        self.chat_id = chat_id
        self.user_id = user_id
        self.joined_date = joined_date or datetime.now()

    def __repr__(self):
        return f"<ChatMember {self.chat_member_id}>"


class ChatMemberSQLModel(ChatMember, BaseModel):
    __tablename__ = "chat_member"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    joined_date = Column(DateTime, default=datetime.now, nullable=False)
    user = relationship("UserSQLModel", foreign_keys=[user_id])


class ChatMemberJSONModel(ChatMember):

    def __init__(self, id, chat_id, user_id, joined_date=None):
        super().__init__(chat_id, user_id, joined_date)
        self.id = id

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "chat_id": self.chat_id,
            "user_id": self.user_id,
            "joined_date": self.joined_date
        }

    @classmethod
    def from_dict(cls, data:dict):
        return cls(**data)
