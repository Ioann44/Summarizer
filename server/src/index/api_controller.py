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
        return {key: value for key, value in text_obj.items() if key in "preview sourceFile".split()}


@index_api.route("/poll", methods=["GET"])
def get_statistic_poll():
    uuid = service.random.choice(
        "b36ad9b4204e4912b14126f7da4b94b1 355c53630d374e10999a4226faf88917 0f40fcba84c34ac7b564a8a8f25b2949 ade4e766f01c40b2ace0aff0bc974007 37eb8e0344fb41e3848a3673e0fac461 4d89a8f78d7549d29e317e056893966e 5501160644f94215b206c3c3fbfabd08 4eddccadd4204128b35c38ea35a39987".split()
    )
    values = service.get_statistic_poll(uuid)
    return flask.jsonify(dict(zip("text good_color perc".split(), values)))


@index_api.route("/poll", methods=["POST"])
def add_poll_result():
    json: Dict[str, Any] = flask.request.json or dict()
    return service.add_poll_obj(json)


@index_api.route("/search", methods=["POST"])
def get_similar_words():
    json: Dict[str, Any] = flask.request.json or dict()
    source_text = json.get("text", "")
    key_word = json.get("word", "")

    if not source_text or source_text.isspace():
        return "Текст для поиска должен быть непустым", 422
    if not key_word or key_word.isspace():
        return "Слово для поиска синонимов не должно быть пустым", 422

    info_msg, res = service.get_similar_words(source_text, key_word)

    if res is None:
        return info_msg, 422

    return {"words": res, "info_msg": info_msg}
