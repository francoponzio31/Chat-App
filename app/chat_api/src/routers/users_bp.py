from flask import Blueprint
from controllers.users_controller import users_controller


users_bp = Blueprint("users_bp", __name__)

users_bp.add_url_rule("/", "get_users", users_controller.get_users, methods=["GET"])

users_bp.add_url_rule("/<int:user_id>", "get_user_by_id", users_controller.get_user_by_id, methods=["GET"])

users_bp.add_url_rule("/", "update_current_user", users_controller.update_current_user, methods=["PATCH"])

users_bp.add_url_rule("/picture", "get_current_user_picture", users_controller.get_current_user_picture, methods=["GET"])

users_bp.add_url_rule("/picture", "update_current_user_picture", users_controller.update_current_user_picture, methods=["PUT"])
