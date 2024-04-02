from flask import request, jsonify
from services.messages_service import messages_service
from marshmallow import ValidationError
from utilities.customExceptions import UserIsNotInChat
from utilities.logger import logger


class MessagesController:

    def get_chat_messages(self, chat_id):
        try:
            messages = messages_service.get_chat_messages(chat_id)
            return jsonify({"message": "Succesful search", "messages": messages})
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"message": "Error getting messages"}), 500


    def send_message(self):
        try:        
            new_message = messages_service.send_message(request.json)
            return jsonify({"message": "Succesful creation", "message": new_message})
        except ValidationError as ex:
            return jsonify({"message": f"Invalid data: {ex.messages}"}), 400
        except UserIsNotInChat:
            return jsonify({"message": "The sender user is not in the chat"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"message": "Error sending message"}), 500


messages_controller = MessagesController()