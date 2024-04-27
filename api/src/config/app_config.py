from dotenv import load_dotenv
from utilities.utils import get_env_value


load_dotenv()

class BaseConfig:
    
    ENV = get_env_value("ENV", "not_set")

    # APP
    DEBUG = get_env_value("DEBUG", False)
    TESTING = get_env_value("TESTING", False)
    SECRET_KEY = get_env_value("SECRET_KEY", "not_set")
    HOST = get_env_value("API_HOST", "127.0.0.1")
    PORT = get_env_value("API_PORT", 8080)
    
    # AUTH
    JWT_KEY = get_env_value("JWT_KEY", "not_set")
    VERIFY_JWT_EXPIRATION = get_env_value("VERIFY_JWT_EXPIRATION", True)

    # REPORITORIES
    DATA_PERSISTENCE_TYPE = get_env_value("DATA_PERSISTENCE_TYPE", "not_set")
    DATA_PERSISTENCE_PATH = get_env_value("DATA_PERSISTENCE_PATH", "not_set")
    DB_URL = get_env_value("DB_URL", None)
    
    # INTEGRATIONS
    FILESERVER_BASE_URL = get_env_value("FILESERVER_BASE_URL", "not_set")


class DevelopmentConfig(BaseConfig):
    ...


class ProductionConfig(BaseConfig):
    ...


env = get_env_value("ENV")
if env == "PROD":
    config = ProductionConfig
else:
    config = DevelopmentConfig