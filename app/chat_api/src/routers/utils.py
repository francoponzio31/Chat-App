from routers.general_bp import general_bp
from routers.auth_bp import auth_bp
from routers.users_bp import users_bp
from routers.chats_bp import chats_bp
from werkzeug.exceptions import HTTPException
from utilities.logger import logger
from utilities.responses import get_error_response
from utilities import status_codes


def init_routes(app):
    app.register_blueprint(general_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(chats_bp, url_prefix="/api/chats")

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return get_error_response(status=status_codes.HTTP_404_NOT_FOUND)

    @app.errorhandler(Exception)
    def internal_server_error(error):
        logger.exception(str(Exception))
        # HTTP errors are not handled (like 401 status code):
        if isinstance(error, HTTPException):
            return error
        return get_error_response(status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
