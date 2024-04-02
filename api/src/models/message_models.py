from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from repositories.sql_connection import BaseModel
from datetime import datetime


class Message:

    def __init__(self, chat_id, sender_user_id, content, joined_date=None):
        self.chat_id = chat_id
        self.sender_user_id = sender_user_id
        self.content = content
        self.joined_date = joined_date or datetime.now()

    def __repr__(self):
        return f"<Message {self.message_id}>"


class MessageSQLModel(Message, BaseModel):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    sender_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)
    sent_date = Column(DateTime, default=datetime.now, nullable=False)
    sender_user = relationship("UserSQLModel", foreign_keys=[sender_user_id])


class MessageJSONModel(Message):

    def __init__(self, id, chat_id, sender_user_id, content, joined_date=None):
        super().__init__(chat_id, sender_user_id, content, joined_date)
        self.id = id

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "chat_id": self.chat_id,
            "sender_user_id": self.sender_user_id,
            "content": self.content,
            "joined_date": self.joined_date,
        }

    @classmethod
    def from_dict(cls, data:dict):
        return cls(**data)
