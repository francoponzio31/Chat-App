from flask import Blueprint
from controllers.messages_controller import messages_controller


messages_bp = Blueprint("messages_bp", __name__)

messages_bp.add_url_rule("/<int:chat_id>", "get_chat_messages", messages_controller.get_chat_messages, methods=["GET"])

messages_bp.add_url_rule("/", "send_message", messages_controller.send_message, methods=["POST"])
