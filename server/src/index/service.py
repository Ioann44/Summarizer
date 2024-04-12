import math
import os
import sys
from typing import List, Optional, Tuple
from hashlib import sha256
from uuid import uuid4

location = os.path.dirname(__file__)
sys.path.append(location + "/../../../summarizer/")

from src.common.global_utils import env
from prelearned_summarizer.summarizer import summarize_extended as summarize_prelearned  # type: ignore
from primitive_summarizer import summarize as summarize_primitive  # type: ignore
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
            sumr_list = summarize_prelearned(mn_service.get_text(str(text_obj.sourceFile)))
            sumr_uuid = uuid4().hex
            mn_service.save_pickle(sumr_list, sumr_uuid)
            db_service.update({"hash": text_obj.hash, "vectFile": sumr_uuid})
            print(f"Computed vectFile for {hash}")
        # get res
        result = get_result(str(text_obj.vectFile or sumr_uuid), compression_mul)  # type: ignore
        print(f"Used vectFile for {hash}")
    # is count
    else:
        if text_obj.primFile is None:
            sumr_list = summarize_primitive(mn_service.get_text(str(text_obj.sourceFile)))
            sumr_uuid = uuid4().hex
            mn_service.save_pickle(sumr_list, sumr_uuid)
            db_service.update({"hash": text_obj.hash, "primFile": sumr_uuid})
            print(f"Computed primFile for {hash}")
        # get res
        result = get_result(str(text_obj.primFile or sumr_uuid), compression_mul)  # type: ignore
        print(f"Used primFile for {hash}")

    return result


def get_text_obj(hash) -> dict[str, Optional[str]]:
    text_obj = db_service.get_one(hash)
    return {c.name: getattr(text_obj, c.name) for c in Text.__table__.columns}


def get_result(uuid: str, k: float) -> Tuple[str, str]:
    precomp_obj: List[Tuple[str, int]] = mn_service.load_pickle(uuid)
    full_len = len(precomp_obj)
    result_len = math.ceil(full_len / k)
    result_text = " ".join(sent for sent, _ in sorted(precomp_obj[:result_len], key=lambda x: x[1]))
    return result_text, f"Количество предложений в исходном тексте: {full_len}, сокращённом - {result_len}"
