from repositories.chats.chats_repository_interface import ChatsRepositoryInterface
from repositories.sql_base_repository import SQLBaseRepository
from models.chat_models import ChatSQLModel
from models.chat_member_models import ChatMemberSQLModel
from repositories.sql_connection import with_db_session, scoped_session



class SQLChatRepository(SQLBaseRepository, ChatsRepositoryInterface):

    @property
    def Model(self) -> ChatSQLModel:
        return ChatSQLModel


    @with_db_session
    def get_user_chats(self, user_id:int, db_session:scoped_session=None) -> list[ChatSQLModel]:
        chats = db_session.query(self.Model).join(ChatMemberSQLModel).filter(ChatMemberSQLModel.user_id == user_id).all()
        return chats
