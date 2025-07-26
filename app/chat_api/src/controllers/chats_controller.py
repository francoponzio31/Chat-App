from flask import request, g, Response
from utilities import status_codes
from schemas.chat_schemas import (
    chats_output_schema,
    chats_search_params_schema,
    create_chat_body_schema,
    messages_read_body_schema,
    messages_search_params_schema,
    chat_output_schema,
    message_body_schema,
    message_output_schema,
    messages_output_schema,
)
from services.chats_service import chats_service
from utilities.responses import get_success_response, get_error_response
from utilities import status_codes
from utilities.custom_exceptions import EntityNotFoundError, UserIsNotInChatError, DirectChatWithSameUserError
from marshmallow import ValidationError
from auth.auth import login_required
from utilities.logger import logger


class ChatsController:

    @login_required
    def get_current_user_chats(self) -> tuple[Response, int]:
        try:
            user_id = g.user.id
            search_params = chats_search_params_schema.load(request.args)
            chats, total_count = chats_service.get_user_chats(user_id, **search_params)
            chats_output = chats_output_schema.dump(chats)
            return get_success_response(status=status_codes.HTTP_200_OK, chats=chats_output, total_count=total_count)
        except ValidationError as ex:
            return get_error_response(status=status_codes.HTTP_400_BAD_REQUEST, message=f"Invalid data: {ex.messages}")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


    @login_required
    def create_chat(self) -> tuple[Response, int]:
        try:
            new_chat_data = create_chat_body_schema.load(request.json)
            new_chat = chats_service.create_chat(**new_chat_data)
            new_chat_output = chat_output_schema.dump(new_chat)
            return get_success_response(status=status_codes.HTTP_201_CREATED, chat=new_chat_output)
        except ValidationError as ex:
            return get_error_response(status=status_codes.HTTP_400_BAD_REQUEST, message=f"Invalid data: {ex.messages}")
        except EntityNotFoundError as ex:
            return get_error_response(status=status_codes.HTTP_404_NOT_FOUND, message=str(ex))
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


    @login_required
    def get_chat_by_id(self, chat_id:int) -> tuple[Response, int]:
        try:
            user_id = g.user.id
            chat = chats_service.get_chat_by_id(chat_id, user_id)
            chat_output = chat_output_schema.dump(chat)
            return get_success_response(status=status_codes.HTTP_200_OK, chat=chat_output)
        except ValidationError as ex:
            return get_error_response(status=status_codes.HTTP_400_BAD_REQUEST, message=f"Invalid data: {ex.messages}")
        except EntityNotFoundError as ex:
            return get_error_response(status=status_codes.HTTP_404_NOT_FOUND, message=str(ex))
        except UserIsNotInChatError:
            return get_error_response(status=status_codes.HTTP_403_FORBIDDEN, message="User is not in the chat")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


    @login_required
    def get_direct_chat_id_with_second_user(self, second_user_id:int) -> tuple[Response, int]:
        try:
            user_id = g.user.id
            chat_id, is_new_chat = chats_service.get_direct_chat_id_with_second_user(user_id, second_user_id)
            return get_success_response(status=status_codes.HTTP_200_OK, chat_id=chat_id, is_new_chat=is_new_chat)
        except EntityNotFoundError as ex:
            return get_error_response(status=status_codes.HTTP_404_NOT_FOUND, message=str(ex))          
        except DirectChatWithSameUserError as ex:
            return get_error_response(status=status_codes.HTTP_404_NOT_FOUND, message="You can't have a direct chat with yourself")          
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


    @login_required
    def get_chat_messages(self, chat_id:int) -> tuple[Response, int]:
        try:
            user_id = g.user.id
            search_params = messages_search_params_schema.load(request.args)
            messages, total_count = chats_service.get_chat_messages(chat_id, user_id, **search_params)
            messages_output = messages_output_schema.dump(messages)
            return get_success_response(status=status_codes.HTTP_200_OK, messages=messages_output, total_count=total_count)
        except EntityNotFoundError as ex:
            return get_error_response(status=status_codes.HTTP_404_NOT_FOUND, message=str(ex))
        except UserIsNotInChatError:
            return get_error_response(status=status_codes.HTTP_403_FORBIDDEN, message="User is not in the chat")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


    @login_required
    def send_message(self, chat_id:int) -> tuple[Response, int]:
        try:
            user_id = g.user.id
            new_message_data = message_body_schema.load(request.json)
            new_message = chats_service.send_message(user_id, chat_id, **new_message_data)
            new_message_output = message_output_schema.dump(new_message)
            return get_success_response(status=status_codes.HTTP_201_CREATED, new_message=new_message_output)
        except ValidationError as ex:
            return get_error_response(status=status_codes.HTTP_400_BAD_REQUEST, message=f"Invalid data: {ex.messages}")
        except UserIsNotInChatError:
            return get_error_response(status=status_codes.HTTP_403_FORBIDDEN, message="User is not in the chat")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


    @login_required
    def record_message_read(self) -> tuple[Response, int]:
        try:
            user_id = g.user.id
            message_ids = messages_read_body_schema.load(request.json)
            chats_service.record_message_read(user_id, **message_ids)
            return get_success_response(status=status_codes.HTTP_201_CREATED)
        except ValidationError as ex:
            return get_error_response(status=status_codes.HTTP_400_BAD_REQUEST, message=f"Invalid data: {ex.messages}")
        except EntityNotFoundError as ex:
            return get_error_response(status=status_codes.HTTP_404_NOT_FOUND, message=str(ex))
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


chats_controller = ChatsController()