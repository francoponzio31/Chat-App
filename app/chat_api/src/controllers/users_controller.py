from flask import request, g, Response
from utilities import status_codes
from schemas.user_schemas import user_body_schema, picture_body_schema, user_search_params_schema, user_output_schema, users_output_schema
from services.users_service import users_service
from utilities.responses import get_success_response, get_error_response
from marshmallow import ValidationError
from utilities.custom_exceptions import EntityNotFoundError
from auth.auth import login_required
from utilities.logger import logger


class UsersController:
        
    @login_required
    def get_users(self) -> tuple[Response, int]:
        try:
            search_params = user_search_params_schema.load(request.args)
            users_result, total_count = users_service.get_users(**search_params)
            users_output = users_output_schema.dump(users_result)
            return get_success_response(status=status_codes.HTTP_200_OK, users=users_output, total_count=total_count)
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


    @login_required
    def get_user_by_id(self, user_id:int) -> tuple[Response, int]:
        try:
            user = users_service.get_user_by_id(user_id)
            user_output = user_output_schema.dump(user)
            return get_success_response(status=status_codes.HTTP_200_OK, user=user_output)
        except EntityNotFoundError as ex:
            return get_error_response(status=status_codes.HTTP_404_NOT_FOUND, message=str(ex))
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


    @login_required
    def update_current_user(self) -> tuple[Response, int]:
        try:
            user_id = g.user.id
            updated_user_data = user_body_schema.load(request.json, partial=True)
            updated_user = users_service.update_user(user_id, **updated_user_data)
            user_output = user_output_schema.dump(updated_user)
            return get_success_response(status=status_codes.HTTP_200_OK, user=user_output)
        except ValidationError as ex:
            return get_error_response(status=status_codes.HTTP_400_BAD_REQUEST, message=f"Invalid data: {ex.messages}")
        except EntityNotFoundError as ex:
            return get_error_response(status=status_codes.HTTP_404_NOT_FOUND, message=str(ex))
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


    @login_required
    def get_current_user_picture(self) -> tuple[Response, int]:
        try:
            user_id = g.user.id
            picture_content = users_service.get_user_picture(user_id)
            return get_error_response(status=status_codes.HTTP_200_OK, picture_content=picture_content)
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


    @login_required
    def update_current_user_picture(self) -> tuple[Response, int]:
        try:
            user_id = g.user.id
            picture_data = picture_body_schema.load(request.json)
            picture_id = users_service.update_user_picture(user_id, **picture_data)
            return get_error_response(status=status_codes.HTTP_200_OK, picture_id=picture_id)
        except ValidationError as ex:
            return get_error_response(status=status_codes.HTTP_400_BAD_REQUEST, message=f"Invalid data: {ex.messages}")
        except EntityNotFoundError as ex:
            return get_error_response(status=status_codes.HTTP_404_NOT_FOUND, message=str(ex))
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


users_controller = UsersController()