from repositories import chats_repository
from schemas.chat_schema import chat_schema, chats_schema
from utilities.customExceptions import IsGroupModificationError, GroupNameModificationError


class ChatsService:

    def get_user_chats(self, user_id) -> list[dict]:
        chats = chats_repository.get_user_chats(user_id)
        return chats_schema.dump(chats)


    def create_chat(self, new_chat_data:dict) -> dict:
        new_chat_data = chat_schema.load(new_chat_data)
        new_chat = chats_repository.create_one(new_chat_data)
        return chat_schema.dump(new_chat)


    def update_chat(self, chat_id:int, updated_chat_data:dict) -> dict:
        updated_chat_data = chat_schema.load(updated_chat_data, partial=True)
        
        if "is_group" in updated_chat_data:
            raise IsGroupModificationError
        
        chat = chats_repository.get_by_id(chat_id)
        if not chat.is_group and "group_name" in updated_chat_data:
            raise GroupNameModificationError

        chat = chats_repository.update_one(chat_id, updated_chat_data)
        return chat_schema.dump(chat)


chats_service = ChatsService()