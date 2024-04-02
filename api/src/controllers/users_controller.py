from flask import request, jsonify
from services.users_service import users_service
from marshmallow import ValidationError
from utilities.customExceptions import EntityNotFoundError, EmailAlreadyRegistered
from utilities.logger import logger


class UsersController:
        
    def get_users(self):
        try:
            users = users_service.get_users()
            return jsonify({"message": "Succesful search", "users": users})
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"message": "Error getting users"}), 500


    def get_user_by_id(self, user_id):
        try:
            user = users_service.get_user_by_id(user_id)
            return jsonify({"message": "Succesful search", "user": user})
        except EntityNotFoundError:
            return jsonify({"message": f"User with id {user_id} not found"}), 404
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"message": "Error getting user"}), 500


    def create_user(self):
        try:
            new_user = users_service.create_user(request.json)
            return jsonify({"message": "Succesful creation", "user": new_user})
        except ValidationError as ex:
            return jsonify({"message": f"Invalid data: {ex.messages}"}), 400
        except EmailAlreadyRegistered:
            return jsonify({"message": "The email is already registered"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"message": "Error creating user"}), 500


    def update_user(self, user_id):
        try:       
            updated_user = users_service.update_user(user_id, request.json)
            return jsonify({"message": "Succesful update", "user": updated_user})
        except ValidationError as ex:
            return jsonify({"message": f"Invalid data: {ex.messages}"}), 400
        except EntityNotFoundError:
            return jsonify({"message": f"User with id {user_id} not found"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"message": "Error updating user"}), 500


    def delete_user(self, user_id):
        try:
            users_service.delete_user(user_id)
            return jsonify({"message": "Succesful delete"})
        except EntityNotFoundError:
            return jsonify({"message": f"User with id {user_id} not found"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"message": "Error deleting user"}), 500


users_controller = UsersController()