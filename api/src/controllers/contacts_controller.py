from flask import request, jsonify
from services.contacts_service import contacts_service
from marshmallow import ValidationError
from utilities.customExceptions import EntityNotFoundError, ContactAlreadyRegisteredError
from utilities.logger import logger


class ContactsController:

    def get_user_contacts(self, user_id):
        try:
            contacts = contacts_service.get_user_contacts(user_id)
            return jsonify({"message": "Succesful search", "contacts": contacts})
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"message": "Error getting contacts"}), 500


    def create_contact(self):
        try:        
            new_contact = contacts_service.create_contact(request.json)
            return jsonify({"message": "Succesful creation", "contact": new_contact})
        except ValidationError as ex:
            return jsonify({"message": f"Invalid data: {ex.messages}"}), 400
        except ContactAlreadyRegisteredError:
            return jsonify({"message": "The user already has the contact registered"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"message": "Error creating contact"}), 500


    def delete_contact(self, contact_id):
        try:
            contacts_service.delete_contact(contact_id)
            return jsonify({"message": "Succesful delete"})
        except EntityNotFoundError:
            return jsonify({"message": f"Contact with id {contact_id} not found"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"message": "Error deleting contact"}), 500


contacts_controller = ContactsController()