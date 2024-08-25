from repositories import chat_members_repository
from utilities.custom_exceptions import MemberAlreadyInChatError


class ChatMembersService:

    def get_chat_members(self, chat_id:int) -> dict:
        return chat_members_repository.get_chat_members(chat_id)


    def add_member(self, chat_id:int, user_id:int) -> dict:
        member_already_in_chat = chat_members_repository.check_if_user_is_in_chat(chat_id, user_id)
        if member_already_in_chat:
            raise MemberAlreadyInChatError
        return chat_members_repository.create_one(chat_id=chat_id, user_id=user_id)


    def delete_member(self, chat_member_id:int) -> None:
        chat_members_repository.delete_one(chat_member_id)


chat_members_service = ChatMembersService()