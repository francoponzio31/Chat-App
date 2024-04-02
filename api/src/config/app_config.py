from dotenv import load_dotenv
from utilities.utils import get_env_value


load_dotenv()

class BaseConfig:
    DEBUG = get_env_value("DEBUG", False)
    TESTING = get_env_value("TESTING", False)
    SECRET_KEY = get_env_value("SECRET_KEY")
    HOST = get_env_value("API_HOST", "127.0.0.1")
    PORT = get_env_value("API_PORT", 8080)
    DATA_PERSISTENCE_TYPE = get_env_value("DATA_PERSISTENCE_TYPE")


class DevelopmentConfig(BaseConfig):
    ...


class ProductionConfig(BaseConfig):
    ...


env = get_env_value("ENV")
if env == "PROD":
    app_config = ProductionConfig
else:
    app_config = DevelopmentConfig