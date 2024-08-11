from schemas.message_schema import message_schema, messages_schema
from repositories import messages_repository
from repositories import chat_members_repository
from utilities.custom_exceptions import UserIsNotInChatError


class MessagesService:

    def get_chat_messages(self, chat_id:int) -> dict:
        messages = messages_repository.get_chat_messages(chat_id)
        return messages_schema.dump(messages)


    def send_message(self, new_message_data:dict) -> dict:
        new_message_data = message_schema.load(new_message_data)

        user_is_in_chat = chat_members_repository.check_if_user_is_in_chat(
            chat_id = new_message_data["chat_id"],
            user_id = new_message_data["sender_user_id"],
        )
        if not user_is_in_chat:
            raise UserIsNotInChatError

        new_message = messages_repository.create_one(new_message_data)
        return message_schema.dump(new_message)


messages_service = MessagesService()
