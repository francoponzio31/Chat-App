from flask import Blueprint
from controllers.chats_controller import chats_controller


chats_bp = Blueprint("chats_bp", __name__)

chats_bp.add_url_rule("/<int:user_id>", "get_user_chats", chats_controller.get_user_chats, methods=["GET"])

chats_bp.add_url_rule("/", "create_chat", chats_controller.create_chat, methods=["POST"])

chats_bp.add_url_rule("/<int:chat_id>", "update_chat", chats_controller.update_chat, methods=["PATCH"])
