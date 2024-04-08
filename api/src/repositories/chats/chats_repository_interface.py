from abc import ABC, abstractmethod

from models.chat_models import Chat


class ChatsRepositoryInterface(ABC):

    @abstractmethod
    def get_all(self) -> list[Chat]:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def get_by_id(self, chat_id:int) -> Chat:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def create_one(self, new_chat_data:dict) -> Chat:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def update_one(self, chat_id:int, updated_chat_data:dict) -> Chat:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def delete_one(self, chat_id:int) -> None:
        raise NotImplementedError("Implement this method on all subclasses.")

    @abstractmethod
    def get_user_chats(self, user_id) -> list[Chat]:
        raise NotImplementedError("Implement this method on all subclasses.")
