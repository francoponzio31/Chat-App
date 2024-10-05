from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from repositories.sql_connection import BaseModel
from datetime import datetime


class ChatModel(BaseModel):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_group = Column(Boolean, nullable=False)
    group_name = Column(String(50), nullable=True)
    creation_date = Column(DateTime, default=datetime.now, nullable=False)
    chat_members = relationship("ChatMemberModel", lazy="joined")

    def __str__(self) -> str:
        return "Chat"
    

class MessageModel(BaseModel):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    sender_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(String, nullable=False)
    sent_date = Column(DateTime, default=datetime.now, nullable=False)
    sender_user = relationship("UserModel", foreign_keys=[sender_user_id], lazy="joined")

    def __str__(self) -> str:
        return "Message"


class ChatMemberModel(BaseModel):
    __tablename__ = "chat_member"
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    joined_date = Column(DateTime, default=datetime.now, nullable=False)
    user = relationship("UserModel", foreign_keys=[user_id], lazy="joined")

    def __str__(self) -> str:
        return "Chat Member"


class MessageReadModel(BaseModel):
    __tablename__ = "message_reads"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    message_id = Column(Integer, ForeignKey("messages.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    read_at = Column(DateTime, default=datetime.now, nullable=False)

    def __str__(self) -> str:
        return "Message read"
