from flask import jsonify, Response
from datetime import datetime
from http import HTTPStatus
from humps import camelize


def _get_base_response(status:int, message:str="", **kwargs) -> tuple[Response, int]:
    body = camelize({
        "message": message or HTTPStatus(status).phrase,
        **kwargs
    })
    return jsonify(body), status


def get_success_response(status:int, message:str="", **kwargs) -> tuple[Response, int]:
    return _get_base_response(message=message, status=status, **kwargs)


def get_error_response(status:int, message:str="", **kwargs) -> tuple[Response, int]:
    return _get_base_response(message=message, status=status, timestamp=datetime.now().isoformat(), **kwargs)
