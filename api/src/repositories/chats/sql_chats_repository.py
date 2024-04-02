from repositories.chats.chats_repository_interface import ChatsRepositoryInterface
from repositories.sql_base_repository import SQLBaseRepository
from models.chat_models import ChatSQLModel
from models.chat_member_models import ChatMemberSQLModel
from typing import List


class SQLChatRepository(SQLBaseRepository, ChatsRepositoryInterface):

    @property
    def Model(self) -> ChatSQLModel:
        return ChatSQLModel


    def get_user_chats(self, user_id) -> List[ChatSQLModel]:
        chats = ChatSQLModel.query.join(ChatMemberSQLModel).filter(ChatMemberSQLModel.user_id == user_id).all()
        return chats
