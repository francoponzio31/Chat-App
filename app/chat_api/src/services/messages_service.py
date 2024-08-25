from repositories import messages_repository
from repositories import chat_members_repository
from utilities.custom_exceptions import UserIsNotInChatError


class MessagesService:

    def get_chat_messages(self, chat_id:int) -> dict:
        return messages_repository.get_chat_messages(chat_id)


    def send_message(self, chat_id:int, sender_user_id:int, content:str) -> dict:
        user_is_in_chat = chat_members_repository.check_if_user_is_in_chat(
            chat_id = chat_id,
            user_id = sender_user_id,
        )
        if not user_is_in_chat:
            raise UserIsNotInChatError

        return messages_repository.create_one(chat_id=chat_id, sender_user_id=sender_user_id, content=content)


messages_service = MessagesService()
