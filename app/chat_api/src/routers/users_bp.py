from flask import Blueprint
from controllers.users_controller import users_controller


users_bp = Blueprint("users_bp", __name__)

users_bp.add_url_rule("/", "get_users", users_controller.get_users, methods=["GET"])

users_bp.add_url_rule("/<int:user_id>", "get_user_by_id", users_controller.get_user_by_id, methods=["GET"])

users_bp.add_url_rule("/<int:user_id>", "update_user", users_controller.update_user, methods=["PATCH"])

users_bp.add_url_rule("/picture/<int:user_id>", "get_user_picture", users_controller.get_user_picture, methods=["GET"])

users_bp.add_url_rule("/picture/<int:user_id>", "update_user_picture", users_controller.update_user_picture, methods=["PUT"])

users_bp.add_url_rule("/<int:user_id>", "delete_user", users_controller.delete_user, methods=["DELETE"])
