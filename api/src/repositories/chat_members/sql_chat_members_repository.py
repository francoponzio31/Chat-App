from repositories.chat_members.chat_members_repository_interface import ChatMembersRepositoryInterface
from repositories.sql_base_repository import SQLBaseRepository
from models.chat_member_models import ChatMemberSQLModel
from sqlalchemy.orm import joinedload
from typing import List


class SQLChatMemberRepository(SQLBaseRepository, ChatMembersRepositoryInterface):

    @property
    def Model(self) -> ChatMemberSQLModel:
        return ChatMemberSQLModel


    def get_chat_members(self, chat_id) -> List[ChatMemberSQLModel]:
        chat_members = ChatMemberSQLModel.query.options(joinedload(ChatMemberSQLModel.user)).filter_by(chat_id=chat_id).all()
        return chat_members


    def check_if_user_is_in_chat(self, chat_id:int, user_id:int) -> bool:
        chat_member = ChatMemberSQLModel.query.filter_by(
            chat_id=chat_id,
            user_id=user_id
        ).one_or_none()
        return chat_member is not None
