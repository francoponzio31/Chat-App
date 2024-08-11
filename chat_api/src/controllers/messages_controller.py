from flask import request, jsonify, Response
from services.messages_service import messages_service
from marshmallow import ValidationError
from utilities.custom_exceptions import UserIsNotInChatError
from utilities.logger import logger
from auth.validators import login_required

class MessagesController:

    @login_required
    def get_chat_messages(self, chat_id:int) -> tuple[Response, int]:
        try:
            messages = messages_service.get_chat_messages(chat_id)
            return jsonify({"success": True, "message": "Successful search", "messages": messages}), 200
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error getting messages"}), 500


    @login_required
    def send_message(self) -> tuple[Response, int]:
        try:        
            new_message = messages_service.send_message(request.json)
            return jsonify({"success": True, "message": "Successful creation", "new_message": new_message}), 200
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except UserIsNotInChatError:
            return jsonify({"success": False, "message": "The sender user is not in the chat"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error sending message"}), 500


messages_controller = MessagesController()