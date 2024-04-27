from abc import ABC, abstractmethod
from models.message_models import Message


class MessagesRepositoryInterface(ABC):

    @abstractmethod
    def get_all(self) -> list[Message]:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def get_by_id(self, message_id:int) -> Message:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def create_one(self, new_message_data:dict) -> Message:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def update_one(self, message_id:int, updated_message_data:dict) -> Message:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def delete_one(self, message_id:int) -> None:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def get_chat_messages(self, chat_id:int) -> list[Message]:
        raise NotImplementedError("Implement this method on all subclasses.")
