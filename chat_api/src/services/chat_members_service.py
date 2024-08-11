from schemas.chat_member_schema import chat_member_schema, chat_members_schema
from repositories import chat_members_repository
from utilities.custom_exceptions import MemberAlreadyInChatError


class ChatMembersService:

    def get_chat_members(self, chat_id:int) -> dict:
        chat_members = chat_members_repository.get_chat_members(chat_id)
        return chat_members_schema.dump(chat_members)


    def add_member(self, new_member_data:dict) -> dict:
        new_member_data = chat_member_schema.load(new_member_data)
        member_already_in_chat = chat_members_repository.check_if_user_is_in_chat(
            chat_id=new_member_data["chat_id"],
            user_id=new_member_data["user_id"]
        )
        if member_already_in_chat:
            raise MemberAlreadyInChatError
        new_member = chat_members_repository.create_one(new_member_data)
        return chat_member_schema.dump(new_member)


    def delete_member(self, chat_member_id:int) -> None:
        chat_members_repository.delete_one(chat_member_id)


chat_members_service = ChatMembersService()