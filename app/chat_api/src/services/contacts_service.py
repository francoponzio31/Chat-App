from repositories import contacts_repository
from utilities.custom_exceptions import ContactAlreadyRegisteredError


class ContactsService:

    def get_user_contacts(self, user_id:int) -> list[dict]:
        return contacts_repository.get_user_contacts(user_id)


    def create_contact(self, user_id:int, contact_user_id:int) -> dict:
        contact_already_registered = contacts_repository.check_already_registered_contact(
            user_id=user_id,
            contact_user_id=contact_user_id
        )
        if contact_already_registered:
            raise ContactAlreadyRegisteredError
        return contacts_repository.create_one(
            user_id=user_id,
            contact_user_id=contact_user_id
        )


    def delete_contact(self, contact_id:int) -> None:
        contacts_repository.delete_one(contact_id)


contacts_service = ContactsService()