from dotenv import load_dotenv
from utilities.utils import get_env_value


load_dotenv()

class Config:

    ENV = get_env_value("ENV", "not_set")

    # APP
    HOST = get_env_value("API_HOST", "127.0.0.1")
    PORT = get_env_value("API_PORT", 8080)
    DEBUG = get_env_value("DEBUG", False)
    TESTING = get_env_value("TESTING", False)
    SECRET_KEY = get_env_value("SECRET_KEY", "not_set")
    LOG_LEVEL = get_env_value("LOG_LEVEL", "INFO")

    # AUTH
    JWT_KEY = get_env_value("JWT_KEY", "not_set")
    VERIFY_JWT_EXPIRATION = get_env_value("VERIFY_JWT_EXPIRATION", True)

    # DB
    DB_URL = get_env_value("DB_URL", "not_set")

    # REDIS
    REDIS_HOST = get_env_value("REDIS_HOST", "not_set")
    REDIS_PORT = get_env_value("REDIS_PORT", 6379)
    REDIS_DB = get_env_value("REDIS_DB", 0)
    CACHE_TTL = get_env_value("CACHE_TTL", 300)
    
    # INTEGRATIONS
    FILESERVER_BASE_URL = get_env_value("FILESERVER_BASE_URL", "not_set")
    MAILER_BASE_URL = get_env_value("MAILER_BASE_URL", "not_set")
    CLIENT_BASE_URL = get_env_value("CLIENT_BASE_URL", "not_set")


config = Config()