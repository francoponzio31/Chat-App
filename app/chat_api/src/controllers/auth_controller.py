from flask import request, g, Response
from utilities import status_codes
from schemas.auth_schemas import login_body_schema, signup_body_schema, email_validation_body_schema, current_user_output_schema, login_output_schema
from services.auth_service import auth_service
from marshmallow import ValidationError
from utilities.responses import get_success_response, get_error_response
from utilities.custom_exceptions import InvalidCredentialsError, EmailNotVerifiedError, EmailAlreadyRegisteredError, InvalidVerificationTokenError
from utilities.logger import logger
from auth.auth import login_required
from utilities.custom_exceptions import EntityNotFoundError


class AuthController:

    def login(self) -> tuple[Response, int]:
        try:
            credentials = login_body_schema.load(request.json)
            token, user = auth_service.login(**credentials)
            login_output = login_output_schema.dump({"token": token, "user": user})
            return get_success_response(status=status_codes.HTTP_200_OK, **login_output)
        except ValidationError as ex:
            return get_error_response(status=status_codes.HTTP_400_BAD_REQUEST, message=f"Invalid data: {ex.messages}")
        except EmailNotVerifiedError:
            return get_error_response(status=status_codes.HTTP_403_FORBIDDEN, message="Email not verified")
        except InvalidCredentialsError:
            return get_error_response(status=status_codes.HTTP_401_UNAUTHORIZED, message="Wrong email or password")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


    def signup(self) -> tuple[Response, int]:
        try:
            new_user_data = signup_body_schema.load(request.json)
            auth_service.signup(**new_user_data)
            return get_success_response(status=status_codes.HTTP_201_CREATED)
        except ValidationError as ex:
            return get_error_response(status=status_codes.HTTP_400_BAD_REQUEST, message=f"Invalid data: {ex.messages}")
        except EmailAlreadyRegisteredError:
            return get_error_response(status=status_codes.HTTP_409_CONFLICT, message="The email is already registered")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


    def verify_email(self, user_id: int) -> tuple[Response, int]:
        try:
            email_validation_data = email_validation_body_schema.load(request.json)
            auth_service.verify_email(user_id, **email_validation_data)
            return get_success_response(status=status_codes.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return get_error_response(status=status_codes.HTTP_400_BAD_REQUEST, message=f"Invalid data: {ex.messages}")
        except EntityNotFoundError as ex:
            return get_error_response(status=status_codes.HTTP_404_NOT_FOUND, message=str(ex))
        except InvalidVerificationTokenError:
            return get_error_response(status=status_codes.HTTP_403_FORBIDDEN, message="Invalid email verification token")
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


    @login_required
    def current_user(self) -> tuple[Response, int]:
        try:
            current_user = g.user
            user_output = current_user_output_schema.dump(current_user)
            return get_success_response(status=status_codes.HTTP_200_OK, user=user_output)
        except ValidationError as ex:
            return get_error_response(status=status_codes.HTTP_400_BAD_REQUEST, message=f"Invalid data: {ex.messages}")
        except EntityNotFoundError as ex:
            return get_error_response(status=status_codes.HTTP_404_NOT_FOUND, message=str(ex))
        except Exception as ex:
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


auth_controller = AuthController()