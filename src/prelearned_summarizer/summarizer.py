import os
import sys
from typing import List, Tuple
from collections import Counter

location = os.path.dirname(__file__)
sys.path.append(location + "/../")

import tools


def get_grade_fast(sentence: Counter, total_counter: Counter, total_words) -> float:
    """Works in O(n), low correlation with similar sentences length"""
    grade = 0
    for word_key, word_count in sentence.items():
        grade += word_count * (total_counter[word_key] - word_count)
    grade /= sum(sentence.values())
    return grade


def get_grade_slow(sentence: Counter, counters: List[Counter]) -> float:
    """Works in O(n^2), hight correlation with similar sentences length"""
    grade = 0
    sentence_len = sum(sentence.values())
    for other_sentence in counters:
        cur_grade = 0
        for word_key, word_count in sentence.items():
            cur_grade += word_count * other_sentence.get(word_key, 0)
        cur_grade /= sentence_len + sum(other_sentence.values())
        grade += cur_grade
    return grade


def summarize(text: str):
    sentences = tools.split_to_sentences(text)
    lemmas_matrix = tools.get_lemmatized_matrix(text)
    counters = [Counter(sentence) for sentence in lemmas_matrix]
    total_counter = Counter()
    for counter in counters:
        total_counter += counter
    # choice one of grade functions
    index_with_grade = [
        (
            i,
            # get_grade_fast(counter, total_counter, total_words)
            get_grade_slow(counter, counters),
        )
        for i, counter in enumerate(counters)
    ]
    index_with_grade.sort(key=lambda i_grade: i_grade[1])
    # lower sentence len in 2 times
    summarized_index_with_grade = index_with_grade[: len(lemmas_matrix) // 2]
    summarized_index_with_grade.sort()
    return " ".join(sentences[i] for i, _ in summarized_index_with_grade)


if __name__ == "__main__":
    with open(location + "/../../other/input.txt", "r", encoding="utf-8") as file:
        input_text = file.read()
    res = summarize(input_text)
    with open(location + "/../../other/output.txt", "a", encoding="utf-8") as file:
        file.write("\n" * 2)
        file.write(res)
