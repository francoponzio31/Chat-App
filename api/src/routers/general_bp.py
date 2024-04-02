from flask import Blueprint, jsonify


general_bp = Blueprint('general', __name__)


@general_bp.get("/alive")
def alive():
    return jsonify({"message": "App running!"})

@general_bp.get("/")
def index():
    return jsonify({"message": "Welcome to the Chat API"})
