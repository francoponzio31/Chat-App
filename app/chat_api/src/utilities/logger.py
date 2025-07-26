import logging
from config.app_config import config
from logging.handlers import RotatingFileHandler


def setup_logging():
    
    logger = logging.getLogger("App Logger")
    logger.setLevel(config.LOG_LEVEL.upper())
    formatter = logging.Formatter("- %(asctime)s - %(name)s - %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(config.LOG_LEVEL.upper())
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if config.ENV == "PROD":
        # File handler
        file_handler = RotatingFileHandler("logs/prod_logs.log", maxBytes=1048576, backupCount=5)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger


logger = setup_logging()