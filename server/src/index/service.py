import math
import os
import random
import sys
from typing import Any, Dict, List, Optional, Tuple
from hashlib import sha256
from uuid import uuid4

location = os.path.dirname(__file__)
sys.path.append(location + "/../../../summarizer/")

from src.index import db_text_service, db_poll_service
from src.common.global_utils import env
from prelearned_summarizer.summarizer import summarize_extended as summarize_prelearned  # type: ignore
from prelearned_summarizer.summarizer import get_similar_words_graded  # type: ignore
from primitive_summarizer import summarize as summarize_primitive  # type: ignore
from src.index import mn_service
from src.index.entities import PollRes, Text


def summarize(text: str, method_is_vec: bool, compression_mul: float) -> Tuple[str, str, str]:
    hash = sha256(text.encode()).hexdigest()
    print(f"Received hash {hash}. ", end="")

    text_obj = db_text_service.get_with_date_update(hash)
    # no hash
    if text_obj is None:
        source_file_name = uuid4().hex + ".txt"
        mn_service.put_text(text, source_file_name)
        text_dct = {
            "hash": hash,
            "preview": text[0:125] + (text[125:128] if len(text) <= 128 else "..."),
            "sourceFile": source_file_name,
        }
        text_obj = db_text_service.add(text_dct)
        print("Saved")
    else:
        print("Already exists")

    # is vec
    if method_is_vec:
        if str(text_obj.vectFile) == "Processing":
            print(f"Request of hash {hash} denied because it is processing now")
            return "", "Этот текст обрабатывается прямо сейчас, повторите запрос через пару минут", hash
        elif text_obj.vectFile is None:
            db_text_service.update({"hash": text_obj.hash, "vectFile": "Processing"})
            sumr_list = summarize_prelearned(mn_service.get_text(str(text_obj.sourceFile)))
            sumr_uuid = uuid4().hex
            mn_service.save_pickle(sumr_list, sumr_uuid)
            db_text_service.update({"hash": text_obj.hash, "vectFile": sumr_uuid})
            print(f"Computed vectFile for {hash}")
        # get res
        result = get_result(str(text_obj.vectFile or sumr_uuid), compression_mul)  # type: ignore
        print(f"Used vectFile for {hash}")
    # is count
    else:
        if str(text_obj.primFile) == "Processing":
            print(f"Request of hash {hash} denied because it is processing now")
            return "", "Этот текст обрабатывается прямо сейчас, повторите запрос через пару минут", hash
        elif text_obj.primFile is None:
            db_text_service.update({"hash": text_obj.hash, "primFile": "Processing"})
            sumr_list = summarize_primitive(mn_service.get_text(str(text_obj.sourceFile)))
            sumr_uuid = uuid4().hex
            mn_service.save_pickle(sumr_list, sumr_uuid)
            db_text_service.update({"hash": text_obj.hash, "primFile": sumr_uuid})
            print(f"Computed primFile for {hash}")
        # get res
        result = get_result(str(text_obj.primFile or sumr_uuid), compression_mul)  # type: ignore
        print(f"Used primFile for {hash}")

    return *result, hash


def get_text_obj(hash) -> Dict[str, Optional[str]]:
    text_obj = db_text_service.get_one(hash)
    return {c.name: getattr(text_obj, c.name) for c in Text.__table__.columns}


def get_result(uuid: str, k: float) -> Tuple[str, str]:
    precomp_obj: List[Tuple[str, int, float]] = mn_service.load_pickle(uuid)
    full_len = sum(len(sent) for sent, _, _ in precomp_obj)
    result_len = math.ceil(full_len / k)
    accum_len = 0
    accum_i = 0
    while accum_len < result_len:
        accum_len += len(precomp_obj[accum_i][0])
        accum_i += 1
    result_text = " ".join(sent for sent, _, _ in sorted(precomp_obj[:accum_i], key=lambda x: x[1]))
    return (
        result_text,
        f"Количество символов предложений в исходном тексте: {full_len}, сокращённом - {accum_len}",
    )


def get_statistic_poll(uuid: str) -> Tuple[str, str, int]:
    precomp_obj: List[Tuple[str, int, float]] = mn_service.load_pickle(uuid)
    good_i_lst = [i for _, i, _ in precomp_obj[: math.ceil(len(precomp_obj) * 0.1)]]
    bad_i_lst = [i for _, i, _ in precomp_obj[math.floor(len(precomp_obj) * 0.9) :]]
    good_i = random.choice(good_i_lst)
    bad_i = random.choice(bad_i_lst)
    precomp_obj.sort(key=lambda x: x[1])
    colors = ["blue", "pink"]
    good_color = "blue"
    if random.random() > 0.5:
        colors.reverse()
        good_color = "red"
    sentences = [sent for sent, _, _ in precomp_obj]

    sentences[good_i] = f'<span style="background-color: light{colors[0]};">{sentences[good_i]}</span>'
    sentences[bad_i] = f'<span style="background-color: light{colors[1]};">{sentences[bad_i]}</span>'

    supr_in_perc = 100 - round(max(precomp_obj[bad_i][2], 0) / max(1, precomp_obj[good_i][2]) * 100)
    return " ".join(sentences), good_color, supr_in_perc


def add_poll_obj(poll_dict) -> Dict[str, Optional[str]]:
    poll_obj = db_poll_service.add(poll_dict)
    return {c.name: getattr(poll_obj, c.name) for c in PollRes.__table__.columns}


def get_similar_words(text, sim_word, threshold) -> Tuple[str, Any]:
    print(f"Search for word {sim_word}")
    res = get_similar_words_graded(text, sim_word, threshold)

    if res is None:
        print(f"Word {sim_word} not found in model")
        return "Для заданного слова вектор не был найден", None
    else:
        print(f"Word {sim_word} was found in model")
        return f"Выделены все слова, имеющие сходство не менее {threshold}%", res
