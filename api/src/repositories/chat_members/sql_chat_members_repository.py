from repositories.chat_members.chat_members_repository_interface import ChatMembersRepositoryInterface
from repositories.sql_base_repository import SQLBaseRepository
from models.chat_member_models import ChatMemberSQLModel
from repositories.sql_connection import with_db_session, scoped_session
from sqlalchemy.orm import joinedload



class SQLChatMemberRepository(SQLBaseRepository[ChatMemberSQLModel], ChatMembersRepositoryInterface):

    @property
    def Model(self) -> ChatMemberSQLModel:
        return ChatMemberSQLModel


    @with_db_session
    def get_chat_members(self, chat_id:int, db_session:scoped_session=None) -> list[ChatMemberSQLModel]:
        chat_members = db_session.query(self.Model).options(joinedload(ChatMemberSQLModel.user)).filter_by(chat_id=chat_id).all()
        return chat_members


    @with_db_session
    def check_if_user_is_in_chat(self, chat_id:int, user_id:int, db_session:scoped_session=None) -> bool:
        chat_member = db_session.query(self.Model).filter_by(
            chat_id=chat_id,
            user_id=user_id
        ).one_or_none()
        return chat_member is not None
