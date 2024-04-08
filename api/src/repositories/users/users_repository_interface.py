from abc import ABC, abstractmethod

from models.user_models import User


class UsersRepositoryInterface(ABC):

    @abstractmethod
    def get_all(self) -> list[User]:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def get_by_id(self, user_id:int) -> User:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def create_one(self, new_user_data:dict) -> User:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def update_one(self, user_id:int, updated_user_data:dict) -> User:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def delete_one(self, user_id:int) -> None:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def get_by_email(self, user_email:str, raise_if_not_found:bool) -> User:
        raise NotImplementedError("Implement this method on all subclasses.")
