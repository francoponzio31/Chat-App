from flask import request, jsonify, Response
from services.chats_service import chats_service
from utilities.customExceptions import EntityNotFoundError, IsGroupModificationError, GroupNameModificationError
from marshmallow import ValidationError
from utilities.validators import token_required
from utilities.logger import logger


class ChatsController:

    @token_required
    def get_user_chats(self, user_id:int) -> tuple[Response, int]:
        try:
            chats = chats_service.get_user_chats(user_id)
            return jsonify({"success": True, "message": "Succesful search", "chats": chats}), 200
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error getting chats"}), 500


    @token_required
    def create_chat(self) -> tuple[Response, int]:
        # TODO: agregar la posibilidad de que se pase una lista de miembros al momento de crear el chat y se agreguen de una al chat
        try:
            new_chat = chats_service.create_chat(request.json)
            return jsonify({"success": True, "message": "Succesful creation", "chat": new_chat}), 200
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error creating chat"}), 500


    @token_required
    def update_chat(self, chat_id:int) -> tuple[Response, int]:
        try:
            updated_chat = chats_service.update_chat(chat_id, request.json)
            return jsonify({"success": True, "message": "Succesful update", "chat": updated_chat}), 200
        except IsGroupModificationError:
            return jsonify({"success": False, "message": "The field is_group is read-only and cannot be modified."}), 400
        except GroupNameModificationError:
            return jsonify({"success": False, "message": "The chat is not a group."}), 400
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except EntityNotFoundError:
            return jsonify({"success": False, "message": f"Chat with id {chat_id} not found"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error updating chat"}), 500


chats_controller = ChatsController()