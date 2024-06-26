from flask import request, jsonify, Response
from services.users_service import users_service
from marshmallow import ValidationError
from utilities.custom_exceptions import EntityNotFoundError, EmailAlreadyRegistered
from utilities.validators import token_required
from utilities.logger import logger


class UsersController:
        
    @token_required
    def get_users(self) -> tuple[Response, int]:
        try:
            users = users_service.get_users()
            return jsonify({"success": True, "message": "Succesful search", "users": users}), 200
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error getting users"}), 500


    @token_required
    def get_user_by_id(self, user_id:int) -> tuple[Response, int]:
        try:
            user = users_service.get_user_by_id(user_id)
            return jsonify({"success": True, "message": "Succesful search", "user": user}), 200
        except EntityNotFoundError:
            return jsonify({"success": False, "message": f"User with id {user_id} not found"}), 404
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error getting user"}), 500


    def create_user(self) -> tuple[Response, int]:
        try:
            new_user = users_service.create_user(request.json)
            return jsonify({"success": True, "message": "Succesful creation", "user": new_user}), 200
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except EmailAlreadyRegistered:
            return jsonify({"success": False, "message": "The email is already registered"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error creating user"}), 500


    @token_required
    def update_user(self, user_id:int) -> tuple[Response, int]:
        try:       
            updated_user = users_service.update_user_picture(user_id, request.json)
            return jsonify({"success": True, "message": "Succesful update", "user": updated_user}), 200
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except EntityNotFoundError:
            return jsonify({"success": False, "message": f"User with id {user_id} not found"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error updating user"}), 500


    @token_required
    def get_user_picture(self, user_id:int) -> tuple[Response, int]:
        try:
            picture_content = users_service.get_user_picture(user_id)
            return jsonify({"success": True, "message": "Succesful search", "picture_content": picture_content}), 200
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error getting user picture"}), 500


    @token_required
    def update_user_picture(self, user_id:int) -> tuple[Response, int]:
        try:
            picture_id = users_service.update_user_picture(user_id, request.json)
            return jsonify({"success": True, "message": "Succesful update", "picture_id": picture_id}), 200
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error updating user picture"}), 500


    @token_required
    def delete_user(self, user_id:int) -> tuple[Response, int]:
        try:
            users_service.delete_user(user_id)
            return jsonify({"success": True, "message": "Succesful delete"}), 200
        except EntityNotFoundError:
            return jsonify({"success": False, "message": f"User with id {user_id} not found"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error deleting user"}), 500


users_controller = UsersController()