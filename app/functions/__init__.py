import functools
from flask import request, jsonify
from dotenv import load_dotenv
import os
from pipeline.shared_content import logger


load_dotenv()
API_CODE = os.getenv("API_CODE", "")


def api_code_validation(function):
    """
    A decorator which verify api_code is valid by comparing with env variable API_CODE
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        api_code = data.get('api_code', None)
        if api_code != API_CODE:
            logger.warning("api_key auth failed")
            return jsonify({"status": "failed"})

        result = function(*args, **kwargs)
        return result

    return wrapper
