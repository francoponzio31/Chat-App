from repositories.contacts.contacts_repository_interface import ContactsRepositoryInterface
from repositories.json_base_repository import JSONBaseRepository 
from models.contact_models import ContactJSONModel
from repositories.users.json_users_repository import JSONUserRepository
from typing import List


class JSONContactRepository(JSONBaseRepository, ContactsRepositoryInterface):

    def __init__(self) -> None:
        self.users_repository = JSONUserRepository()
        super().__init__(filename="contacts.json")


    @property
    def Model(self) -> ContactJSONModel:
        return ContactJSONModel


    def create_one(self, new_contact_data:dict) -> ContactJSONModel:
        self.users_repository.get_by_id(new_contact_data["contact_user_id"])  # Checks if the contact user exists
        return super().create_one(new_contact_data)


    def get_user_contacts(self, user_id:int) -> List[ContactJSONModel]:
        contacts = self.get_all()
        user_contacts = []
        for contact in contacts:
            if contact.user_id == user_id:
                contact.contact_user = self.users_repository.get_by_id(contact.contact_user_id)
                user_contacts.append(contact)
        return user_contacts


    def check_already_registered_contact(self, user_id:int, contact_user_id:int) -> bool:
        contacts = self.get_all()
        searched_contact = None
        for contact in contacts:
            if contact.user_id == user_id and contact.contact_user_id == contact_user_id:
                searched_contact = contact
                break
        return searched_contact is not None
