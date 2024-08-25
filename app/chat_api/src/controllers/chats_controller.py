from flask import request, jsonify, Response
from schemas.chat_schemas import create_chat_body_schema, update_chat_body_schema, chat_output_schema, chats_output_schema
from services.chats_service import chats_service
from utilities.custom_exceptions import EntityNotFoundError, GroupNameModificationError
from marshmallow import ValidationError
from auth.validators import login_required
from utilities.logger import logger


class ChatsController:

    @login_required
    def get_user_chats(self, user_id:int) -> tuple[Response, int]:
        try:
            chats = chats_service.get_user_chats(user_id)
            chats_output = chats_output_schema.dump(chats)
            return jsonify({"success": True, "message": "Successful search", "chats": chats_output}), 200
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error getting chats"}), 500


    @login_required
    def create_chat(self) -> tuple[Response, int]:
        # TODO: agregar la posibilidad de que se pase una lista de miembros al momento de crear el chat y se agreguen de una al chat
        try:
            new_chat_data = create_chat_body_schema.load(request.json)
            new_chat = chats_service.create_chat(**new_chat_data)
            new_chat_output = chat_output_schema.dump(new_chat)
            return jsonify({"success": True, "message": "Successful creation", "chat": new_chat_output}), 200
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error creating chat"}), 500


    @login_required
    def update_chat(self, chat_id:int) -> tuple[Response, int]:
        try:
            updated_chat_data = update_chat_body_schema.load(request.json, partial=True)
            updated_chat = chats_service.update_chat(chat_id, **updated_chat_data)
            updated_chat_output = chat_output_schema.dump(updated_chat)
            return jsonify({"success": True, "message": "Successful update", "chat": updated_chat_output}), 200
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