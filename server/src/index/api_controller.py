from typing import Any, Dict
import flask
from flask import Blueprint

import src.index.service as service

index_api = Blueprint("index_api", __name__, url_prefix="/api")


@index_api.route("/summarize", methods=["POST"])
def summarize():
    json: Dict[str, Any] = flask.request.json or dict()

    source_text: str = json.get("text", "")
    preferred_method = json.get("method", "")
    try:
        compression_mul = float(json.get("compression_mul", ""))
    except:
        compression_mul = 3

    match preferred_method:
        case "count":
            method_is_vec = False
        case _:
            method_is_vec = True

    if not source_text or source_text.isspace():
        return "Здесь нечего сокращать", 422

    compressed_text, info_msg, hash_value = service.summarize(source_text, method_is_vec, compression_mul)

    return {"text": compressed_text, "info_msg": info_msg, "hash": hash_value}


@index_api.route("/history/<string:hash>", methods=["POST"])
def get_text_obj(hash: str):
    text_obj = service.get_text_obj(hash)
    if text_obj is None:
        return "Данного текста нет либо истёк срок его хранения", 404
    else:
        return {
            key: value for key, value in text_obj.items() if key in "preview sourceFile".split()
        }
