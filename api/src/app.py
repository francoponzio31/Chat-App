from flask import Flask
from flask_cors import CORS
from config.app_config import config
from routers.utils import init_routes, register_error_handlers


def create_app() -> Flask:

    app = Flask(__name__)

    # CONFIG
    app.config.from_object(config)

    # CORS
    CORS(app, resources={r"/api/*": {"origins": [config.CLIENT_BASE_URL]}})

    # DB
    if config.DATA_PERSISTENCE_TYPE == "SQL":
        from repositories.sql_connection import init_db
        with app.app_context():
            init_db()

    # ROUTES
    init_routes(app)

    # ERROR HANDLERS
    register_error_handlers(app)
    
    return app
