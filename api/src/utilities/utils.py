import os
from typing import Any
from datetime import datetime
import bcrypt
import base64


def get_env_value(key:str, default:Any=None) -> Any:
    """Obtains and parses the value of an env"""
    value = os.getenv(key, default)

    if value in ("False", "false"):
        value = False

    elif value in ("True", "true"):
        value = True

    return value


def json_encoder(obj:Any) -> Any:
    """Serialize objects to JSON"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, bytes):
        return r"\x" + obj.hex()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def json_decoder(dict:dict) -> dict:
    """Converts strings in ISO 8601 format to datetime objects"""
    for key, value in dict.items():
        try:
            dict[key] = datetime.fromisoformat(value)
        except (ValueError, TypeError):
            pass
    return dict


def hash_password(password:str) -> bytes:
    """Hash the given password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def compare_hashed_password(password:str, hashed_password:str) -> bool:
    """Compare a plaintext password against a hashed password to verify if they match"""
    if isinstance(hashed_password, str) and hashed_password.startswith(r"\x"):  # Postgress and my JSON repository saves binary data as hexadecimal encoded strings
        hashed_password = bytes.fromhex(hashed_password[2:])
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
