from repositories.contacts.contacts_repository_interface import ContactsRepositoryInterface
from repositories.sql_base_repository import SQLBaseRepository
from models.contact_models import ContactSQLModel
from sqlalchemy.orm import joinedload
from typing import List


class SQLContactRepository(SQLBaseRepository, ContactsRepositoryInterface):

    @property
    def Model(self) -> ContactSQLModel:
        return ContactSQLModel
    

    def get_user_contacts(self, user_id:int) -> List[ContactSQLModel]:
        contacts = ContactSQLModel.query.options(joinedload(ContactSQLModel.contact_user)).filter_by(user_id=user_id).all()
        return contacts


    def check_already_registered_contact(self, user_id:int, contact_user_id:int) -> bool:
        contact = ContactSQLModel.query.filter_by(
            user_id=user_id,
            contact_user_id=contact_user_id
        ).one_or_none()
        return contact is not None
