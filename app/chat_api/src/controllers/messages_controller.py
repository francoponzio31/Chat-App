from flask import request, Response
from http import HTTPStatus
from schemas.message_schemas import message_body_schema, message_output_schema, messages_output_schema
from services.messages_service import messages_service
from utilities.responses import get_success_response, get_error_response
from marshmallow import ValidationError
from utilities.custom_exceptions import UserIsNotInChatError
from utilities.logger import logger
from auth.validators import login_required


class MessagesController:

    @login_required
    def get_chat_messages(self, chat_id:int) -> tuple[Response, int]:
        try:
            messages = messages_service.get_chat_messages(chat_id)
            messages_output = messages_output_schema.dump(messages)
            return get_success_response(status=HTTPStatus.OK.value, messages=messages_output)
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)


    @login_required
    def send_message(self) -> tuple[Response, int]:
        try:
            new_message_data = message_body_schema.load(request.json)
            new_message = messages_service.send_message(**new_message_data)
            new_message_output = message_output_schema.dump(new_message)
            return get_success_response(status=HTTPStatus.CREATED.value, new_message=new_message_output)
        except ValidationError as ex:
            return get_error_response(status=HTTPStatus.BAD_REQUEST.value, message=f"Invalid data: {ex.messages}")
        except UserIsNotInChatError:
            return get_error_response(status=HTTPStatus.CONFLICT.value, message="The sender user is not in the chat")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)


messages_controller = MessagesController()