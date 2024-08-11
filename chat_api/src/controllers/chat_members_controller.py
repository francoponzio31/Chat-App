from flask import request, jsonify, Response
from services.chat_members_service import chat_members_service
from utilities.custom_exceptions import EntityNotFoundError, MemberAlreadyInChatError
from marshmallow import ValidationError
from chat_api.src.auth.validators import login_required
from utilities.logger import logger


class ChatMembersController:

    @login_required
    def get_chat_members(self, chat_id:int) -> tuple[Response, int]:
        try:
            chat_members = chat_members_service.get_chat_members(chat_id)
            return jsonify({"success": True, "message": "Successful search", "chat_members": chat_members}), 200
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error getting chat members"}), 500


    @login_required
    def add_member(self) -> tuple[Response, int]:
        try:
            new_chat_member = chat_members_service.add_member(request.json)
            return jsonify({"success": True, "message": "Successful creation", "chat_member": new_chat_member}), 200
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except MemberAlreadyInChatError:
            return jsonify({"success": False, "message": "The user is already in the chat"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error adding chat member"}), 500


    @login_required
    def delete_member(self, chat_member_id:int) -> tuple[Response, int]:
        try:
            chat_members_service.delete_member(chat_member_id)
            return jsonify({"success": True, "message": "Successful delete"}), 200
        except EntityNotFoundError:
            return jsonify({"success": False, "message": f"Chat member with id {chat_member_id} not found"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error deleting chat member"}), 500


chat_members_controller = ChatMembersController()