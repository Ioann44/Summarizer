import os
import sys
from typing import Tuple

location = os.path.dirname(__file__)
sys.path.append(location + "/../../../summarizer/prelearned_summarizer")

from summarizer import summarize_extended # type: ignore


def summarize_vec_slow(text: str, compression_mul: float) -> Tuple[str, str]:
    res_text, initial_num, res_num = summarize_extended(text, compression_mul, True)
    return res_text, f"Количество предложений в исходном тексте: {initial_num}, сокращённом - {res_num}"
