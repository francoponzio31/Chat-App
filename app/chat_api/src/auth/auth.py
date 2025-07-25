from functools import wraps
from flask import request, current_app, g
from utilities.logger import logger
import jwt
from utilities.responses import get_error_response
from utilities import status_codes
from services.users_service import users_service
from utilities.custom_exceptions import EntityNotFoundError


def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        current_app.config["JWT_KEY"],
        algorithms=["HS256"],
        options={"verify_exp": current_app.config["VERIFY_JWT_EXPIRATION"]}
    )


def login_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = None
        try:
            token = auth_header.split("Bearer ")[1]
        except IndexError:
            return get_error_response(status=status_codes.HTTP_400_BAD_REQUEST, message="Bearer token malformatted")

        if not token:
            return get_error_response(status=status_codes.HTTP_401_UNAUTHORIZED, message="Token is missing!")
        
        try:
            data = decode_token(token)
            g.user = users_service.get_user_by_id(data["user"]["id"])  # User data added to request g object

        except jwt.ExpiredSignatureError:
            return get_error_response(status=status_codes.HTTP_401_UNAUTHORIZED, message="Token has expired!")
        except jwt.InvalidTokenError:
            return get_error_response(status=status_codes.HTTP_401_UNAUTHORIZED, message="Token is invalid!")
        except EntityNotFoundError as ex:
            return get_error_response(status=status_codes.HTTP_401_UNAUTHORIZED, message=f"User with id {data['user']['id']} does not exists")
        except Exception as ex:
            logger.exception("Token decoding error:")
            logger.exception(str(ex))
            return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, message="Unable to verify token")
        
        return function(*args, **kwargs)
    
    return decorated
