from flask import Flask
from config.app_config import app_config
from routers.utils import init_routes, register_error_handlers


def create_app() -> Flask:

    app = Flask(__name__)

    # CONFIG
    app.config.from_object(app_config)

    # DB
    if app.config["DATA_PERSISTENCE_TYPE"] == "SQL":
        from repositories.sql_connection import init_db
        with app.app_context():
            init_db()

    # ROUTES
    init_routes(app)

    # ERROR HANDLERS
    register_error_handlers(app)
    
    return app
