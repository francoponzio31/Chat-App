from repositories.chats.chats_repository_interface import ChatsRepositoryInterface
from repositories.json_base_repository import JSONBaseRepository
from repositories.chat_members.json_chat_members_repository import JSONChatMemberRepository
from models.chat_models import ChatJSONModel
from typing import List


class JSONChatRepository(JSONBaseRepository, ChatsRepositoryInterface):

    def __init__(self):
        self.chat_members_repository = JSONChatMemberRepository()
        super().__init__(filename="chats.json")


    @property
    def Model(self) -> ChatJSONModel:
        return ChatJSONModel


    def get_user_chats(self, user_id) -> List[ChatJSONModel]:

        all_chat_members = self.chat_members_repository.get_all()
        user_chats = []

        for chat_member in all_chat_members:
            if chat_member.id == user_id:
                user_chats.append(
                    self.get_by_id(chat_member.chat_id)
                )

        return user_chats
