from flask import Blueprint
from controllers.auth_controller import auth_controller



auth_bp = Blueprint("auth_bp", __name__)

auth_bp.add_url_rule("/login", "login", auth_controller.login, methods=["POST"])

auth_bp.add_url_rule("/signup", "signup", auth_controller.signup, methods=["POST"])

auth_bp.add_url_rule("/verify-email", "verify-email", auth_controller.verify_email, methods=["POST"])

auth_bp.add_url_rule("/current", "current_user", auth_controller.current_user, methods=["GET"])
