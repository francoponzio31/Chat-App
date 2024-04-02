from routers.general_bp import general_bp
from routers.users_bp import users_bp
from routers.contacts_bp import contacts_bp
from routers.chat_members_bp import chat_members_bp
from routers.chats_bp import chats_bp
from routers.messages_bp import messages_bp
from flask import jsonify
from werkzeug.exceptions import HTTPException


def init_routes(app):
    app.register_blueprint(general_bp, url_prefix="/")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(contacts_bp, url_prefix="/api/contacts")
    app.register_blueprint(chat_members_bp, url_prefix="/api/chat-members")
    app.register_blueprint(chats_bp, url_prefix="/api/chats")
    app.register_blueprint(messages_bp, url_prefix="/api/messages")


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"message": "Resource not found"}), 404

    @app.errorhandler(Exception)
    def internal_server_error(error):
        # HTTP errors are not handled (like 401 status code):
        if isinstance(error, HTTPException):
            return error
        return jsonify({"message": "Internal server error"}), 500
