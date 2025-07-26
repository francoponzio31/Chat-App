from repositories.chats_repository import chats_repository
from repositories.cache_repository import cache_repository
from models.chat_models import ChatModel, MessageModel
from utilities.custom_exceptions import UserIsNotInChatError, DirectChatWithSameUserError
from utilities.logger import logger


USERS_CHATS_LIST_CACHE_KEY = "user_chats:{user_id}"

class ChatsService:

    def get_user_chats(self, user_id:int, limit:int|None=None, offset:int|None=None, type:str|None=None) -> tuple[list[ChatModel], int]:
        return chats_repository.get_user_chats(user_id, limit, offset, type)


    def create_chat(self, is_group:bool, group_name:str|None, chat_members_ids:list=[]) -> ChatModel:
        return chats_repository.create_chat(is_group=is_group, group_name=group_name, chat_members_ids=chat_members_ids)


    def get_chat_by_id(self, chat_id:int, user_id:int) -> list[ChatModel]:
        self.check_if_user_is_in_chat(chat_id, user_id)
        return chats_repository.get_by_id(chat_id)
    

    def get_direct_chat_id_with_second_user(self, user_id:int, second_user_id:int) -> tuple[int, bool]:

        is_new_chat = False

        if user_id == second_user_id:
            raise DirectChatWithSameUserError

        chat = chats_repository.get_direct_chat_with_second_user(user_id, second_user_id)
        if not chat:
            chat = self.create_chat(
                is_group=False,
                group_name=None,
                chat_members_ids=[user_id, second_user_id]
            )
            is_new_chat = True

        return chat.id, is_new_chat


    def get_chat_messages(self, chat_id:int, user_id:int, limit:int|None=None, offset:int|None=None) -> list[MessageModel]:
        self.check_if_user_is_in_chat(chat_id, user_id)
        return chats_repository.get_chat_messages(chat_id, user_id, limit, offset)


    def send_message(self, sender_user_id:int, chat_id:int, content:str) -> MessageModel:
        self.check_if_user_is_in_chat(chat_id, sender_user_id)
        return chats_repository.send_message(chat_id=chat_id, sender_user_id=sender_user_id, content=content)


    def record_message_read(self, user_id:int, messages_id:list[str]):
        chats_repository.record_message_read(user_id=user_id, messages_id=messages_id)


    def check_if_user_is_in_chat(self, chat_id: int, user_id: int):
        cache_key = USERS_CHATS_LIST_CACHE_KEY.format(user_id=user_id)
        
        # Check in cache first
        user_cached_chats_list = cache_repository.get(cache_key) or []
        if chat_id in user_cached_chats_list:
            logger.debug(f"User {user_id} is in chat {chat_id} (cached)")
            return

        # If not in cache, check in database and populate cache
        user_is_in_chat = chats_repository.check_if_user_is_in_chat(chat_id=chat_id, user_id=user_id)
        
        # Update cache
        if user_is_in_chat:
            cache_repository.set(cache_key, user_cached_chats_list + [chat_id])
        
        if not user_is_in_chat:
            raise UserIsNotInChatError


chats_service = ChatsService()