from schemas.contact_schema import contact_schema, contacts_schema
from repositories import contacts_repository
from utilities.customExceptions import ContactAlreadyRegisteredError


class ContactsService:

    def get_user_contacts(self, user_id) -> list[dict]:
        contacts = contacts_repository.get_user_contacts(user_id)
        return contacts_schema.dump(contacts)


    def create_contact(self, new_contact_data:dict) -> dict:
        new_contact_data = contact_schema.load(new_contact_data)
        contact_already_registered = contacts_repository.check_already_registered_contact(
            user_id=new_contact_data["user_id"],
            contact_user_id=new_contact_data["contact_user_id"]
        )
        if contact_already_registered:
            raise ContactAlreadyRegisteredError
        new_contact = contacts_repository.create_one(new_contact_data)
        return contact_schema.dump(new_contact)


    def delete_contact(self, contact_id:int) -> None:
        contacts_repository.delete_one(contact_id)


contacts_service = ContactsService()