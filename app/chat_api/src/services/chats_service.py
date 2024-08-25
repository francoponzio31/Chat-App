from repositories import chats_repository
from utilities.custom_exceptions import GroupNameModificationError


class ChatsService:

    def get_user_chats(self, user_id) -> list[dict]:
        return chats_repository.get_user_chats(user_id)


    def create_chat(self, is_group:bool, group_name:str|None) -> dict:
        return chats_repository.create_one(is_group=is_group, group_name=group_name)


    def update_chat(self, chat_id:int, **kwargs) -> dict:               
        chat = chats_repository.get_by_id(chat_id)
        if not chat.is_group and "group_name" in kwargs:
            raise GroupNameModificationError

        return chats_repository.update_one(chat_id, **kwargs)


chats_service = ChatsService()