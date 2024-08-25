from functools import wraps
from flask import request, jsonify, current_app, g
from utilities.logger import logger
import jwt
from typing import Union


def login_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = None
        try:
            token = auth_header.split("Bearer ")[1]
        except IndexError:
            return jsonify({"success": False, "message": "Bearer token malformatted."}), 400

        if not token:
            return jsonify({"success": False, "message": "Token is missing!"}), 401
        
        try:
            data = jwt.decode(
                token,
                current_app.config["JWT_KEY"],
                algorithms=["HS256"],
                options={"verify_exp": current_app.config["VERIFY_JWT_EXPIRATION"]}
            )
            g.user = data["user"]     # User data added to request g object

        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "message": "Token is invalid!"}), 401
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Unable to verify token."}), 500
        
        return function(*args, **kwargs)
    
    return decorated


def role_required(role:Union[str, list]):
    def decorator(function):
        @wraps(function)
        def decorated(*args, **kwargs):
            if not hasattr(request, "user"):
                return jsonify({"success": False, "message": "The user is not authenticated"}), 401

            if isinstance(role, list) and request.user["role"] not in role:
                return jsonify({"success": False, "message": f"The user must have one of the following roles: {role}"}), 403
            elif isinstance(role, str) and request.user["role"] != role:
                return jsonify({"success": False, "message": f"The user must have the following role: {role}"}), 403
            else:
                return function(*args, **kwargs)

        return decorated
    return decorator
