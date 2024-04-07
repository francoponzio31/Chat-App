from flask import request, jsonify, Response
from services.chat_members_service import chat_members_service
from utilities.customExceptions import EntityNotFoundError, MemberAlreadyInChat
from marshmallow import ValidationError
from utilities.validators import token_required
from utilities.logger import logger


class ChatMembersController:

    @token_required
    def get_chat_members(self, chat_id:int) -> Response:
        try:
            chat_members = chat_members_service.get_chat_members(chat_id)
            return jsonify({"success": True, "message": "Succesful search", "chat_members": chat_members})
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error getting chat members"}), 500


    @token_required
    def add_member(self) -> Response:
        try:
            new_chat_member = chat_members_service.add_member(request.json)
            return jsonify({"success": True, "message": "Succesful creation", "chat_member": new_chat_member})
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except MemberAlreadyInChat:
            return jsonify({"success": False, "message": "The user is already in the chat"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error adding chat member"}), 500


    @token_required
    def delete_member(self, chat_member_id:int) -> Response:
        try:
            chat_members_service.delete_member(chat_member_id)
            return jsonify({"success": True, "message": "Succesful delete"})
        except EntityNotFoundError:
            return jsonify({"success": False, "message": f"Chat member with id {chat_member_id} not found"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error deleting chat member"}), 500


chat_members_controller = ChatMembersController()