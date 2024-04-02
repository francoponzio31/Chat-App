from flask import Blueprint
from controllers.contacts_controller import contacts_controller


contacts_bp = Blueprint("contacts_bp", __name__)

contacts_bp.add_url_rule("/<int:user_id>", "get_user_contacts", contacts_controller.get_user_contacts, methods=["GET"])

contacts_bp.add_url_rule("/", "create_contact", contacts_controller.create_contact, methods=["POST"])

contacts_bp.add_url_rule("/<int:contact_id>", "delete_contact", contacts_controller.delete_contact, methods=["DELETE"])
