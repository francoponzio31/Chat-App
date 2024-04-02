import os
from typing import Any
from datetime import datetime


def get_env_value(key:str, default:Any=None) -> Any:
    """Obtains and parses the value of an env"""
    value = os.getenv(key, default)

    if value in ("False", "false"):
        value = False

    elif value in ("True", "true"):
        value = True

    return value


def datetime_encoder(obj: datetime) -> str:
    """Converts datetime objects into string representations for JSON"""
    try:
        return obj.isoformat()
    except AttributeError:
        raise AttributeError(f"Object of type {type(obj)} is not serializable in JSON")


def datetime_decoder(dict:dict) -> dict:
    """Converts strings in ISO 8601 format to datetime objects"""
    for key, value in dict.items():
        try:
            dict[key] = datetime.fromisoformat(value)
        except (ValueError, TypeError):
            pass
    return dict