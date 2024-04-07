from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from repositories.sql_connection import BaseModel
from datetime import datetime


class Contact:

    def __init__(self, user_id, contact_user_id, added_date=None):
        self.user_id = user_id
        self.contact_user_id = contact_user_id
        self.added_date = added_date or datetime.now()

    def __repr__(self):
        return f"<Contact {self.user_id} -> {self.contact_user_id}>"


class ContactSQLModel(Contact, BaseModel):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contact_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    added_date = Column(DateTime, default=datetime.now, nullable=False)
    contact_user = relationship("UserSQLModel", foreign_keys=[contact_user_id])


class ContactJSONModel(Contact):

    def __init__(self, id, user_id, contact_user_id, added_date=None):
        super().__init__(user_id, contact_user_id, added_date)
        self.id = id

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "contact_user_id": self.contact_user_id,
            "added_date": self.added_date
        }

    @classmethod
    def from_dict(cls, data:dict):
        return cls(**data)
