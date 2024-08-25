from flask import request, g, jsonify, Response
from schemas.auth_schemas import login_body_schema, signup_body_schema, email_validation_body_schema, current_user_output_schema
from services.auth_service import auth_service
from marshmallow import ValidationError
from utilities.custom_exceptions import InvalidCredentialsError, EmailNotVerifiedError, EmailAlreadyRegisteredError, InvalidVerificationTokenError
from utilities.logger import logger
from auth.validators import login_required
from utilities.custom_exceptions import EntityNotFoundError


class AuthController:

    def login(self) -> tuple[Response, int]:
        try:
            credentials = login_body_schema.load(request.json)
            token = auth_service.login(**credentials)
            return jsonify({"success": True, "message": "Successful login", "token": token}), 200
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except EmailNotVerifiedError:
            return jsonify({"success": False, "message": "Email not verified"}), 403
        except InvalidCredentialsError:
            return jsonify({"success": False, "message": "Wrong email or password"}), 401
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Login error"}), 500


    def signup(self) -> tuple[Response, int]:
        try:
            new_user_data = signup_body_schema.load(request.json)
            auth_service.signup(**new_user_data)
            return jsonify({"success": True, "message": "Successful signup, verification email sent"}), 200
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except EmailAlreadyRegisteredError:
            return jsonify({"success": False, "message": "The email is already registered"}), 409
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Signup error"}), 500


    def verify_email(self) -> tuple[Response, int]:
        try:
            email_validation_data = email_validation_body_schema.load(request.json)
            auth_service.verify_email(**email_validation_data)
            return jsonify({"success": True, "message": "Successful verification"}), 200
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except EntityNotFoundError:
            return jsonify({"success": False, "message": "User with given id not found"}), 404
        except InvalidVerificationTokenError:
            return jsonify({"success": False, "message": "Invalid email verification token"}), 403
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Verification error"}), 500


    @login_required
    def current_user(self) -> tuple[Response, int]:
        try:
            user_id = g.user["id"]
            user = auth_service.current_user(user_id)
            user_output = current_user_output_schema.dump(user)
            return jsonify({"success": True, "message": "Successful search", "user": user_output}), 200
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except EntityNotFoundError:
            return jsonify({"success": False, "message": f"User with id {user_id} not found"}), 404
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Login error"}), 500


auth_controller = AuthController()