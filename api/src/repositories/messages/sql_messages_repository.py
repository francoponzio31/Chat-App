from repositories.messages.messages_repository_interface import MessagesRepositoryInterface
from repositories.sql_base_repository import SQLBaseRepository
from models.message_models import MessageSQLModel
from repositories.sql_connection import with_db_session, scoped_session
from sqlalchemy.orm import joinedload
from typing import List


class SQLMessageRepository(SQLBaseRepository, MessagesRepositoryInterface):

    @property
    def Model(self) -> MessageSQLModel:
        return MessageSQLModel
    

    @with_db_session
    def get_chat_messages(self, chat_id:int , db_session:scoped_session=None) -> List[MessageSQLModel]:
        messages = db_session.query(self.Model).options(joinedload(MessageSQLModel.sender_user)).filter_by(chat_id=chat_id).all()
        return messages
