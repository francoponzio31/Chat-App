from repositories.messages.messages_repository_interface import MessagesRepositoryInterface
from repositories.sql_base_repository import SQLBaseRepository
from models.message_models import MessageSQLModel
from sqlalchemy.orm import joinedload
from typing import List


class SQLMessageRepository(SQLBaseRepository, MessagesRepositoryInterface):

    @property
    def Model(self) -> MessageSQLModel:
        return MessageSQLModel
    

    def get_chat_messages(self, chat_id:int) -> List[MessageSQLModel]:
        messages = MessageSQLModel.query.options(joinedload(MessageSQLModel.sender_user)).filter_by(chat_id=chat_id).all()
        return messages
