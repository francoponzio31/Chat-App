from flask import request, Response
from http import HTTPStatus
from schemas.chat_member_schemas import chat_member_body_schema, chat_member_output_schema, chat_members_output_schema
from services.chat_members_service import chat_members_service
from utilities.responses import get_success_response, get_error_response
from utilities.custom_exceptions import EntityNotFoundError, MemberAlreadyInChatError
from marshmallow import ValidationError
from auth.validators import login_required
from utilities.logger import logger


class ChatMembersController:

    @login_required
    def get_chat_members(self, chat_id:int) -> tuple[Response, int]:
        try:
            chat_members = chat_members_service.get_chat_members(chat_id)
            chat_members_output = chat_members_output_schema.dump(chat_members)
            return get_success_response(status=HTTPStatus.OK.value, message="Successful search", chat_members=chat_members_output)
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)


    @login_required
    def add_member(self) -> tuple[Response, int]:
        try:
            new_member_data = chat_member_body_schema.load(request.json)
            new_chat_member = chat_members_service.add_member(**new_member_data)
            new_chat_member_output = chat_member_output_schema.dump(new_chat_member)
            return get_success_response(status=HTTPStatus.CREATED.value, message="Successful creation", chat_member=new_chat_member_output)        
        except ValidationError as ex:
            return get_error_response(status=HTTPStatus.BAD_REQUEST.value, message=f"Invalid data: {ex.messages}")
        except MemberAlreadyInChatError:
            return get_error_response(status=HTTPStatus.CONFLICT.value, message="User is already in the chat")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)


    @login_required
    def delete_member(self, chat_member_id:int) -> tuple[Response, int]:
        try:
            chat_members_service.delete_member(chat_member_id)
            return get_success_response(status=HTTPStatus.NO_CONTENT.value)        
        except EntityNotFoundError:
            return get_error_response(status=HTTPStatus.NOT_FOUND.value, message=f"Chat member with id {chat_member_id} not found")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)


chat_members_controller = ChatMembersController()