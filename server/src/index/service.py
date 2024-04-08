import os
import sys
from typing import Optional, Tuple
from hashlib import sha256
from uuid import uuid4

location = os.path.dirname(__file__)
sys.path.append(location + "/../../../summarizer/prelearned_summarizer")

from summarizer import summarize_extended  # type: ignore
from src.index import db_service, mn_service
from src.index.entities import Text


def summarize(text: str, method_is_vec: bool, compression_mul: float) -> Tuple[str, str]:
    hash = sha256(text.encode()).hexdigest()
    print(f"Received hash {hash}. ", end="")

    text_obj = db_service.get_with_date_update(hash)
    # no hash
    if text_obj is None:
        source_file_name = uuid4().hex + ".txt"
        mn_service.put_text(text, source_file_name)
        text_dct = {
            "hash": hash,
            "preview": text[0:125] + (text[125:128] if len(text) <= 128 else "..."),
            "sourceFile": source_file_name,
        }
        text_obj = db_service.add(text_dct)
        print("Saved")
    else:
        print("Already exists")

    # is vec
    if method_is_vec:
        if text_obj.vectFile is None:
            pass
        # get res
    # is count
    else:
        if text_obj.primFile is None:
            pass
        # get res

    # return result

    return summarize_vec_slow(text, compression_mul)


def summarize_vec_slow(text: str, compression_mul: float) -> Tuple[str, str]:
    res_text, initial_num, res_num = summarize_extended(text, compression_mul, True)
    return res_text, f"Количество предложений в исходном тексте: {initial_num}, сокращённом - {res_num}"


def get_text_obj(hash) -> dict[str, Optional[str]]:
    text_obj = db_service.get_one(hash)
    return {c.name: getattr(text_obj, c.name) for c in Text.__table__.columns}
