from flask import request, jsonify, Response
from services.contacts_service import contacts_service
from marshmallow import ValidationError
from utilities.custom_exceptions import EntityNotFoundError, ContactAlreadyRegisteredError
from utilities.validators import token_required
from utilities.logger import logger


class ContactsController:

    @token_required
    def get_user_contacts(self, user_id:int) -> tuple[Response, int]:
        try:
            contacts = contacts_service.get_user_contacts(user_id)
            return jsonify({"success": True, "message": "Succesful search", "contacts": contacts}), 200
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error getting contacts"}), 500


    @token_required
    def create_contact(self) -> tuple[Response, int]:
        try:        
            new_contact = contacts_service.create_contact(request.json)
            return jsonify({"success": True, "message": "Succesful creation", "contact": new_contact}), 200
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except ContactAlreadyRegisteredError:
            return jsonify({"success": False, "message": "The user already has the contact registered"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error creating contact"}), 500


    @token_required
    def delete_contact(self, contact_id:int) -> tuple[Response, int]:
        try:
            contacts_service.delete_contact(contact_id)
            return jsonify({"success": True, "message": "Succesful delete"}), 200
        except EntityNotFoundError:
            return jsonify({"success": False, "message": f"Contact with id {contact_id} not found"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error deleting contact"}), 500


contacts_controller = ContactsController()