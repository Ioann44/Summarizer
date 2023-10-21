from typing import Any, Dict
import flask
from flask import Blueprint

from . import service

index_api = Blueprint("index_api", __name__, url_prefix="/api")


@index_api.route("/summarize", methods=["POST"])
def summarize():
    json: Dict[str, Any] = flask.request.json or dict()

    source_text = json.get("text", "")
    preferred_method = json.get("method", "")
    try:
        compression_mul = int(json.get("compression_mul", ""))
    except:
        compression_mul = 3

    match preferred_method:
        case _:
            method_function = service.summarize_vec_slow

    if not source_text:
        return "Здесь нечего сокращать", 422

    compressed_text, info_msg = method_function(source_text, compression_mul)

    return {"text": compressed_text, "info_msg": info_msg}
