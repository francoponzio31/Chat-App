from flask import request, jsonify
from services.chat_members_service import chat_members_service
from utilities.customExceptions import EntityNotFoundError, MemberAlreadyInChat
from marshmallow import ValidationError
from utilities.logger import logger


class ChatMembersController:

    def get_chat_members(self, chat_id):
        try:
            chat_members = chat_members_service.get_chat_members(chat_id)
            return jsonify({"message": "Succesful search", "chat_members": chat_members})
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"message": "Error getting chat members"}), 500


    def add_member(self):
        try:
            new_chat_member = chat_members_service.add_member(request.json)
            return jsonify({"message": "Succesful creation", "chat_member": new_chat_member})
        except ValidationError as ex:
            return jsonify({"message": f"Invalid data: {ex.messages}"}), 400
        except MemberAlreadyInChat:
            return jsonify({"message": "The user is already in the chat"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"message": "Error adding chat member"}), 500


    def delete_member(self, chat_member_id):
        try:
            chat_members_service.delete_member(chat_member_id)
            return jsonify({"message": "Succesful delete"})
        except EntityNotFoundError:
            return jsonify({"message": f"Chat member with id {chat_member_id} not found"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"message": "Error deleting chat member"}), 500


chat_members_controller = ChatMembersController()