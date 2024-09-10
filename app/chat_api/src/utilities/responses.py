from flask import jsonify, Response
from datetime import datetime
from humps import camelize
from werkzeug.http import HTTP_STATUS_CODES


def _get_base_response(status:int, message:str="", **kwargs) -> tuple[Response, int]:
    response_data = camelize({
        "message": message or HTTP_STATUS_CODES.get(status, ""),
        **kwargs
    })

    return jsonify(response_data), status


def get_success_response(status:int, message:str="", **kwargs) -> tuple[Response, int]:
    return _get_base_response(message=message, status=status, **kwargs)


def get_error_response(status:int, message:str="", **kwargs) -> tuple[Response, int]:
    return _get_base_response(message=message, status=status, timestamp=datetime.now().isoformat(), **kwargs)
