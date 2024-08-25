from flask import request, jsonify, Response
from schemas.user_schemas import user_body_schema, picture_body_schema, user_search_params_schema, user_output_schema, users_output_schema
from services.users_service import users_service
from marshmallow import ValidationError
from utilities.custom_exceptions import EntityNotFoundError
from auth.validators import login_required
from utilities.logger import logger


class UsersController:
        
    @login_required
    def get_users(self) -> tuple[Response, int]:
        try:
            search_params = user_search_params_schema.load(request.args)
            users = users_service.get_users(**search_params)
            users_output = users_output_schema.dump(users)
            return jsonify({"success": True, "message": "Successful search", "users": users_output}), 200
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error getting users"}), 500


    @login_required
    def get_user_by_id(self, user_id:int) -> tuple[Response, int]:
        try:
            user = users_service.get_user_by_id(user_id)
            user_output = user_output_schema.dump(user)
            return jsonify({"success": True, "message": "Successful search", "user": user_output}), 200
        except EntityNotFoundError:
            return jsonify({"success": False, "message": f"User with id {user_id} not found"}), 404
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error getting user"}), 500


    @login_required
    def update_user(self, user_id:int) -> tuple[Response, int]:
        try:
            updated_user_data = user_body_schema.load(request.json, partial=True)
            updated_user = users_service.update_user(user_id, **updated_user_data)
            user_output = user_output_schema.dump(updated_user)
            return jsonify({"success": True, "message": "Successful update", "user": user_output}), 200
        except ValidationError as ex:
            return jsonify({"success": False, "message": f"Invalid data: {ex.messages}"}), 400
        except EntityNotFoundError:
            return jsonify({"success": False, "message": f"User with id {user_id} not found"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error updating user"}), 500


    @login_required
    def get_user_picture(self, user_id:int) -> tuple[Response, int]:
        try:
            picture_content = users_service.get_user_picture(user_id)
            return jsonify({"success": True, "message": "Successful search", "picture_content": picture_content}), 200
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error getting user picture"}), 500


    @login_required
    def update_user_picture(self, user_id:int) -> tuple[Response, int]:
        try:
            picture_data = picture_body_schema.load(request.json)
            picture_id = users_service.update_user_picture(user_id, **picture_data)
            return jsonify({"success": True, "message": "Successful update", "picture_id": picture_id}), 200
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error updating user picture"}), 500


    @login_required
    def delete_user(self, user_id:int) -> tuple[Response, int]:
        try:
            users_service.delete_user(user_id)
            return jsonify({"success": True, "message": "Successful delete"}), 200
        except EntityNotFoundError:
            return jsonify({"success": False, "message": f"User with id {user_id} not found"}), 400
        except Exception as ex:
            logger.exception(str(ex))
            return jsonify({"success": False, "message": "Error deleting user"}), 500


users_controller = UsersController()