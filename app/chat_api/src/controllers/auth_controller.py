from flask import request, g, Response
from http import HTTPStatus
from schemas.auth_schemas import login_body_schema, signup_body_schema, email_validation_body_schema, current_user_output_schema
from services.auth_service import auth_service
from marshmallow import ValidationError
from utilities.responses import get_success_response, get_error_response
from utilities.custom_exceptions import InvalidCredentialsError, EmailNotVerifiedError, EmailAlreadyRegisteredError, InvalidVerificationTokenError
from utilities.logger import logger
from auth.validators import login_required
from utilities.custom_exceptions import EntityNotFoundError


class AuthController:

    def login(self) -> tuple[Response, int]:
        try:
            credentials = login_body_schema.load(request.json)
            token = auth_service.login(**credentials)
            return get_success_response(status=HTTPStatus.OK.value, message="Successful login", token=token)
        except ValidationError as ex:
            return get_error_response(status=HTTPStatus.BAD_REQUEST.value, message=f"Invalid data: {ex.messages}")
        except EmailNotVerifiedError:
            return get_error_response(status=HTTPStatus.FORBIDDEN.value, message="Email not verified")
        except InvalidCredentialsError:
            return get_error_response(status=HTTPStatus.UNAUTHORIZED.value, message="Wrong email or password")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)


    def signup(self) -> tuple[Response, int]:
        try:
            new_user_data = signup_body_schema.load(request.json)
            auth_service.signup(**new_user_data)
            return get_success_response(status=HTTPStatus.CREATED.value, message="Successful signup, verification email sent")
        except ValidationError as ex:
            return get_error_response(status=HTTPStatus.BAD_REQUEST.value, message=f"Invalid data: {ex.messages}")
        except EmailAlreadyRegisteredError:
            return get_error_response(status=HTTPStatus.CONFLICT.value, message="The email is already registered")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)


    def verify_email(self, user_id: int) -> tuple[Response, int]:
        try:
            email_validation_data = email_validation_body_schema.load(request.json)
            auth_service.verify_email(**email_validation_data)
            return get_success_response(status=HTTPStatus.NO_CONTENT.value)
        except ValidationError as ex:
            return get_error_response(status=HTTPStatus.BAD_REQUEST.value, message=f"Invalid data: {ex.messages}")
        except EntityNotFoundError:
            return get_error_response(status=HTTPStatus.NOT_FOUND.value, message=f"User with id {user_id} not found")
        except InvalidVerificationTokenError:
            return get_error_response(status=HTTPStatus.FORBIDDEN.value, message="Invalid email verification token")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)


    @login_required
    def current_user(self) -> tuple[Response, int]:
        try:
            user_id = g.user["id"]
            user = auth_service.current_user(user_id)
            user_output = current_user_output_schema.dump(user)
            return get_success_response(status=HTTPStatus.OK.value, message="Successful search", user=user_output)
        except ValidationError as ex:
            return get_error_response(status=HTTPStatus.BAD_REQUEST.value, message=f"Invalid data: {ex.messages}")
        except EntityNotFoundError:
            return get_error_response(status=HTTPStatus.NOT_FOUND.value, message=f"User with id {user_id} not found")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)




auth_controller = AuthController()