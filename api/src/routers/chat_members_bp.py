from flask import Blueprint
from controllers.chat_members_controller import chat_members_controller


chat_members_bp = Blueprint("chat_members_bp", __name__)

chat_members_bp.add_url_rule("/<int:chat_id>", "get_chat_members", chat_members_controller.get_chat_members, methods=["GET"])

chat_members_bp.add_url_rule("/", "add_chat_member", chat_members_controller.add_member, methods=["POST"])

chat_members_bp.add_url_rule("/<int:chat_member_id>", "delete_chat_member", chat_members_controller.delete_member, methods=["DELETE"])
