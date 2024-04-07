from flask import request, jsonify, Response
from services.auth_service import auth_service
from marshmallow import ValidationError
from utilities.customExceptions import InvalidCredentials
from utilities.logger import logger


class AuthController:

    def login(self) -> Response:
        try:
            token = auth_service.login(request.json)
            return jsonify({"success": True, "message": "Succesful login", "token": token})
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except InvalidCredentials:
            return jsonify({"success": False, "message": "Wrong email or password"}), 401
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Login error"}), 500


auth_controller = AuthController()