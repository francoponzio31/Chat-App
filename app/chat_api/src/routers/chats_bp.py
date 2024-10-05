from flask import Blueprint
from controllers.chats_controller import chats_controller


chats_bp = Blueprint("chats_bp", __name__)

chats_bp.add_url_rule("/", "get_current_user_chats", chats_controller.get_current_user_chats, methods=["GET"])

chats_bp.add_url_rule("/", "create_chat", chats_controller.create_chat, methods=["POST"])

chats_bp.add_url_rule("/<int:chat_id>", "get_chat_by_id", chats_controller.get_chat_by_id, methods=["GET"])

chats_bp.add_url_rule("/direct-chat-with-user/<int:second_user_id>", "get_direct_chat_with_second_user", chats_controller.get_direct_chat_with_second_user, methods=["GET"])

chats_bp.add_url_rule("/<int:chat_id>/messages", "get_chat_messages", chats_controller.get_chat_messages, methods=["GET"])

chats_bp.add_url_rule("/<int:chat_id>/messages", "send_message", chats_controller.send_message, methods=["POST"])

chats_bp.add_url_rule("/messages/record-reading", "record_message_read", chats_controller.record_message_read, methods=["POST"])
