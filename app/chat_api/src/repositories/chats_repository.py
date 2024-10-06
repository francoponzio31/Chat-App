from repositories.base_repository import SQLBaseRepository
from models.chat_models import ChatModel, MessageModel, ChatMemberModel, MessageReadModel
from models.user_models import UserModel
from utilities.custom_exceptions import EntityNotFoundError
from repositories.sql_connection import with_db_session, scoped_session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy import func


class ChatRepository(SQLBaseRepository[ChatModel]):

    @property
    def Model(self) -> ChatModel:
        return ChatModel


    @with_db_session
    def get_user_chats(self, user_id:int, limit:int|None, offset:int|None, chat_type:str, db_session:scoped_session=None) -> tuple[list[ChatModel], int]:
        unread_messages_subquery = db_session.query(
            MessageModel.chat_id,
            func.count(MessageModel.id).label("unread_count")
        ).outerjoin(
            MessageReadModel,
            (MessageReadModel.message_id == MessageModel.id) & (MessageReadModel.user_id == user_id)
        ).filter(
            MessageReadModel.read_at.is_(None)
        ).group_by(MessageModel.chat_id).subquery()

        query = db_session.query(
            self.Model,
            func.coalesce(unread_messages_subquery.c.unread_count, 0).label("unread_messages")
        ).join(
            ChatMemberModel, ChatMemberModel.chat_id == self.Model.id
        ).outerjoin(
            unread_messages_subquery, unread_messages_subquery.c.chat_id == self.Model.id
        ).filter(
            ChatMemberModel.user_id == user_id
        ).order_by(
            func.coalesce(unread_messages_subquery.c.unread_count, 0).desc(),
            self.Model.creation_date.desc()
        )

        if chat_type:
            query = query.filter(self.Model.is_group == (chat_type == "group"))

        total_count = query.count()

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        results = []
        for chat, unread_msg_field in query.all():
            chat.unread_messages = unread_msg_field
            results.append(chat)

        return results, total_count

    

    @with_db_session
    def create_chat(self, is_group:bool, group_name:str|None, chat_members_ids:list, db_session:scoped_session = None) -> ChatModel:
        new_chat = ChatModel(is_group=is_group, group_name=group_name)
        db_session.add(new_chat)
        db_session.flush()

        for member_id in chat_members_ids:
            try:
                new_member = ChatMemberModel(chat_id=new_chat.id, user_id=member_id)
                db_session.add(new_member)
                db_session.flush()
            except IntegrityError:
                raise EntityNotFoundError(f"{str(UserModel())} with id {member_id} does not exists")
        
        return new_chat
        

    @with_db_session
    def get_direct_chat_with_second_user(self, user_id:int, second_user_id:int, db_session:scoped_session = None) -> ChatModel | None:
        chat = db_session.query(self.Model).filter(
            self.Model.is_group == False
        ).join(ChatMemberModel).filter(
            (ChatMemberModel.user_id == user_id) | (ChatMemberModel.user_id == second_user_id)
        ).group_by(self.Model.id).having(
            func.count(ChatMemberModel.user_id.distinct()) == 2
        ).first()

        return chat


    @with_db_session
    def get_chat_messages(self, chat_id:int, user_id:int, limit:int|None, offset:int|None, db_session:scoped_session=None) -> tuple[list[MessageModel], int]:
        chat = self.get_by_id(chat_id)
        
        query = db_session.query(
            MessageModel,
            func.coalesce(MessageReadModel.read_at.isnot(None), False).label("read_by_user")
        ).outerjoin(
            MessageReadModel,
            (MessageReadModel.message_id == MessageModel.id) & (MessageReadModel.user_id == user_id)
        ).options(
            joinedload(MessageModel.sender_user)
        ).filter(
            MessageModel.chat_id == chat.id
        ).order_by(
            MessageModel.sent_date.desc()
        )

        total_count = query.count()

        if offset is not None:
            query = query.offset(offset)
        
        if limit is not None:
            query = query.limit(limit)

        results = []
        for msg, read_by_user_field in query.all():
            msg.read_by_user = read_by_user_field
            results.append(msg)

        return results, total_count


    @with_db_session
    def check_if_user_is_in_chat(self, chat_id:int, user_id:int, db_session:scoped_session=None) -> bool:
        chat_member = db_session.query(ChatMemberModel).filter_by(
            chat_id=chat_id,
            user_id=user_id
        ).one_or_none()
        return chat_member is not None


    @with_db_session
    def send_message(self, chat_id:int, sender_user_id:int, content:str, db_session:scoped_session=None) -> MessageModel:
        new_message = MessageModel(chat_id=chat_id, sender_user_id=sender_user_id, content=content)
        db_session.add(new_message)
        db_session.flush()
        db_session.refresh(new_message)  
        return new_message


    @with_db_session
    def record_message_read(self, user_id:int, messages_id:list[str], db_session:scoped_session=None):
        for message_id in messages_id:
            try:
                message_read = MessageReadModel(user_id=user_id, message_id=message_id)
                db_session.add(message_read)
                db_session.flush()
            except IntegrityError:
                raise EntityNotFoundError(f"{str(MessageReadModel())} with id {messages_id} does not exists")


chats_repository = ChatRepository()
