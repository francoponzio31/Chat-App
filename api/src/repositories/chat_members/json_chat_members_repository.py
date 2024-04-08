from repositories.chat_members.chat_members_repository_interface import ChatMembersRepositoryInterface
from repositories.json_base_repository import JSONBaseRepository
from models.chat_member_models import ChatMemberJSONModel
from repositories.users.json_users_repository import JSONUserRepository



class JSONChatMemberRepository(JSONBaseRepository, ChatMembersRepositoryInterface):

    def __init__(self):
        self.users_repository = JSONUserRepository()
        super().__init__(filename="chat_members.data.json")


    @property
    def Model(self) -> ChatMemberJSONModel:
        return ChatMemberJSONModel


    def get_chat_members(self, chat_id) -> list[ChatMemberJSONModel]:
        all_members = self.get_all()
        chat_members = []
        for member in all_members:
            if member.chat_id == chat_id:
                member.user = self.users_repository.get_by_id(member.user_id)
                chat_members.append(member)
        return chat_members


    def check_if_user_is_in_chat(self, chat_id:int, user_id:int) -> bool:   
        chat_members = self.get_all()
        searched_member = None
        for member in chat_members:
            if member.chat_id == chat_id and member.user_id == user_id:
                searched_member = member
                break
        return searched_member is not None