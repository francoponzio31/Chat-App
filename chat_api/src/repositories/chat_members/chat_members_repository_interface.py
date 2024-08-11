from abc import ABC, abstractmethod
from models.chat_member_models import ChatMember


class ChatMembersRepositoryInterface(ABC):

    @abstractmethod
    def get_all(self) -> list[ChatMember]:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def get_by_id(self, chat_member_id:int) -> ChatMember:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def create_one(self, new_chat_member_data:dict) -> ChatMember:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def update_one(self, chat_member_id:int, updated_chat_member_data:dict) -> ChatMember:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def delete_one(self, chat_member_id:int) -> None:
        raise NotImplementedError("Implement this method on all subclasses.")

    @abstractmethod
    def get_chat_members(self, chat_id) -> list[ChatMember]:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def check_if_user_is_in_chat(self, chat_id:int, user_id:int) -> bool:
        raise NotImplementedError("Implement this method on all subclasses.")
