from abc import ABC, abstractmethod
from typing import List
from models.contact_models import Contact


class ContactsRepositoryInterface(ABC):

    @abstractmethod
    def get_all(self) -> List[Contact]:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def get_by_id(self, contact_id:int) -> Contact:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def create_one(self, new_contact_data:dict) -> Contact:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def update_one(self, contact_id:int, updated_contact_data:dict) -> Contact:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def delete_one(self, contact_id:int) -> None:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def get_user_contacts(self, user_id:int) -> List[Contact]:
        raise NotImplementedError("Implement this method on all subclasses.")


    @abstractmethod
    def check_already_registered_contact(self, user_id:int, contact_user_id:int) -> bool:
        raise NotImplementedError("Implement this method on all subclasses.")
