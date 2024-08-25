from flask import request, jsonify, Response
from schemas.contact_schemas import contact_body_schema, contact_output_schema, contacts_output_schema
from services.contacts_service import contacts_service
from marshmallow import ValidationError
from utilities.custom_exceptions import EntityNotFoundError, ContactAlreadyRegisteredError
from auth.validators import login_required
from utilities.logger import logger


class ContactsController:

    @login_required
    def get_user_contacts(self, user_id:int) -> tuple[Response, int]:
        try:
            contacts = contacts_service.get_user_contacts(user_id)
            contacts_output = contacts_output_schema.dump(contacts)
            return jsonify({"success": True, "message": "Successful search", "contacts": contacts_output}), 200
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error getting contacts"}), 500


    @login_required
    def create_contact(self) -> tuple[Response, int]:
        try:
            new_contact_data = contact_body_schema.load(request.json)
            new_contact = contacts_service.create_contact(**new_contact_data)
            new_contact_output = contact_output_schema.dump(new_contact)
            return jsonify({"success": True, "message": "Successful creation", "contact": new_contact_output}), 200
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except ContactAlreadyRegisteredError:
            return jsonify({"success": False, "message": "The user already has the contact registered"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error creating contact"}), 500


    @login_required
    def delete_contact(self, contact_id:int) -> tuple[Response, int]:
        try:
            contacts_service.delete_contact(contact_id)
            return jsonify({"success": True, "message": "Successful delete"}), 200
        except EntityNotFoundError:
            return jsonify({"success": False, "message": f"Contact with id {contact_id} not found"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error deleting contact"}), 500


contacts_controller = ContactsController()