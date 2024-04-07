from flask import request, jsonify, Response
from services.messages_service import messages_service
from marshmallow import ValidationError
from utilities.customExceptions import UserIsNotInChat
from utilities.logger import logger
from utilities.validators import token_required


class MessagesController:

    @token_required
    def get_chat_messages(self, chat_id:int) -> Response:
        try:
            messages = messages_service.get_chat_messages(chat_id)
            return jsonify({"success": True, "message": "Succesful search", "messages": messages})
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error getting messages"}), 500


    @token_required
    def send_message(self) -> Response:
        try:        
            new_message = messages_service.send_message(request.json)
            return jsonify({"success": True, "message": "Succesful creation", "new_message": new_message})
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except UserIsNotInChat:
            return jsonify({"success": False, "message": "The sender user is not in the chat"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error sending message"}), 500


messages_controller = MessagesController()