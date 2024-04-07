from flask import Blueprint
from controllers.auth_controller import auth_controller



auth_bp = Blueprint("auth_bp", __name__)

auth_bp.add_url_rule("/login", "login", auth_controller.login, methods=["POST"])
