from flask import request, jsonify
from services.chats_service import chats_service
from utilities.customExceptions import EntityNotFoundError, IsGroupModificationError, GroupNameModificationError
from marshmallow import ValidationError
from utilities.logger import logger


class ChatsController:

    def get_user_chats(self, user_id):
        try:
            chats = chats_service.get_user_chats(user_id)
            return jsonify({"message": "Succesful search", "chats": chats})
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"message": "Error getting chats"}), 500


    def create_chat(self):
        # TODO: agregar la posibilidad de que se pase una lista de miembros al momento de crear el chat y se agreguen de una al chat
        try:
            new_chat = chats_service.create_chat(request.json)
            return jsonify({"message": "Succesful creation", "chat": new_chat})
        except ValidationError as ex:
            return jsonify({"message": f"Invalid data: {ex.messages}"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"message": "Error creating chat"}), 500


    def update_chat(self, chat_id):
        try:
            updated_chat = chats_service.update_chat(chat_id, request.json)
            return jsonify({"message": "Succesful update", "chat": updated_chat})
        except IsGroupModificationError:
            return jsonify({"message": "The field is_group is read-only and cannot be modified."}), 400
        except GroupNameModificationError:
            return jsonify({"message": "The chat is not a group."}), 400
        except ValidationError as ex:
            return jsonify({"message": f"Invalid data: {ex.messages}"}), 400
        except EntityNotFoundError:
            return jsonify({"message": f"Chat with id {chat_id} not found"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"message": "Error updating chat"}), 500


chats_controller = ChatsController()