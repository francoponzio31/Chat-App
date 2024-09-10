from flask import request, Response
from http import HTTPStatus
from schemas.user_schemas import user_body_schema, picture_body_schema, user_search_params_schema, user_output_schema, users_output_schema
from services.users_service import users_service
from utilities.responses import get_success_response, get_error_response
from marshmallow import ValidationError
from utilities.custom_exceptions import EntityNotFoundError
from auth.validators import login_required
from utilities.logger import logger


class UsersController:
        
    @login_required
    def get_users(self) -> tuple[Response, int]:
        try:
            search_params = user_search_params_schema.load(request.args)
            users_result, total_count = users_service.get_users(**search_params)
            users_output = users_output_schema.dump(users_result)
            return get_success_response(status=HTTPStatus.OK.value, message="Successful search", users=users_output, total_count=total_count)
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)


    @login_required
    def get_user_by_id(self, user_id:int) -> tuple[Response, int]:
        try:
            user = users_service.get_user_by_id(user_id)
            user_output = user_output_schema.dump(user)
            return get_success_response(status=HTTPStatus.OK.value, message="Successful search", user=user_output)
        except EntityNotFoundError:
            return get_error_response(status=HTTPStatus.NOT_FOUND.value, message=f"User with id {user_id} not found")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)


    @login_required
    def update_user(self, user_id:int) -> tuple[Response, int]:
        try:
            updated_user_data = user_body_schema.load(request.json, partial=True)
            updated_user = users_service.update_user(user_id, **updated_user_data)
            user_output = user_output_schema.dump(updated_user)
            return get_success_response(status=HTTPStatus.OK.value, message="Successful update", user=user_output)
        except ValidationError as ex:
            return get_error_response(status=HTTPStatus.BAD_REQUEST.value, message=f"Invalid data: {ex.messages}")
        except EntityNotFoundError:
            return get_error_response(status=HTTPStatus.NOT_FOUND.value, message=f"User with id {user_id} not found")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)


    @login_required
    def get_user_picture(self, user_id:int) -> tuple[Response, int]:
        try:
            picture_content = users_service.get_user_picture(user_id)
            return get_error_response(status=HTTPStatus.OK.value, message="Successful search", picture_content=picture_content)
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)


    @login_required
    def update_user_picture(self, user_id:int) -> tuple[Response, int]:
        try:
            picture_data = picture_body_schema.load(request.json)
            picture_id = users_service.update_user_picture(user_id, **picture_data)
            return get_error_response(status=HTTPStatus.OK.value, message="Successful update", picture_id=picture_id)
        except ValidationError as ex:
            return get_error_response(status=HTTPStatus.BAD_REQUEST.value, message=f"Invalid data: {ex.messages}")
        except EntityNotFoundError:
            return get_error_response(status=HTTPStatus.NOT_FOUND.value, message=f"User with id {user_id} not found")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)


    @login_required
    def delete_user(self, user_id:int) -> tuple[Response, int]:
        try:
            users_service.delete_user(user_id)
            return get_error_response(status=HTTPStatus.NO_CONTENT.value)
        except EntityNotFoundError:
            return get_error_response(status=HTTPStatus.NOT_FOUND.value, message=f"User with id {user_id} not found")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)


users_controller = UsersController()