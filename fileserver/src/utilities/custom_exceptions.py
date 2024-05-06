from config.app_config import config
from utilities.utils import bytes_to_mb


class InvalidFileID(Exception):
    message = f"Invalid file id format"

class MaxFileSizeExceeded(Exception):
    message = f"Max file size allowed exceeded, max file size: {bytes_to_mb(config.max_file_size):.1f}mb"

class FileTypeNotAccepted(Exception):
    message = f"File type not accepted, accepted file types: {config.allowed_files}"