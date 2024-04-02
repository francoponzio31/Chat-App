import logging
from dotenv import load_dotenv
from utilities.utils import get_env_value
from logging.handlers import RotatingFileHandler


def setup_logging():
    
    load_dotenv()
    env = get_env_value("ENV")

    logger = logging.getLogger("App Logger")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("- %(asctime)s - %(name)s - %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if env == "PROD":
        # File handler
        file_handler = RotatingFileHandler("logs/prod_logs.log", maxBytes=1048576, backupCount=5)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger


logger = setup_logging()