import os
import sys
from typing import List, Tuple
from collections import Counter

from gensim.models import Word2Vec

location = os.path.dirname(__file__)
sys.path.append(location + "/../")

import tools

model = Word2Vec.load(location + "/models/cbow_large.bin")


def get_word_vector(word: str) -> List[float]:
    if word in model.wv:
        return model.wv[word]  # type: ignore
    else:
        return [0.0] * model.vector_size


def make_avg_vector(vectors: List[List[float]]) -> List[float]:
    total_vector = [0.0] * len(vectors[0])
    for vc in vectors:
        for i, vci in enumerate(vc):
            total_vector[i] += vci
    for i in range(len(total_vector)):
        total_vector[i] /= len(vectors)
    return total_vector


def get_cos_distance(vc_a: List[float], vc_b: List[float]) -> float:
    return (
        sum(ai * bi for ai, bi in zip(vc_a, vc_b))
        / sum(ai**2 for ai in vc_a) ** 0.5
        / sum(ab**2 for ab in vc_b) ** 0.5
    )


# def get_grade_fast(sentence: Counter, total_counter: Counter, total_words) -> float:
#     """Works in O(n), low correlation with similar sentences length"""
#     grade = 0
#     for word_key, word_count in sentence.items():
#         grade += word_count * (total_counter[word_key] - word_count)
#     grade /= sum(sentence.values())
#     return grade


def get_grade_slow(sentence: List[float], all_sentences: List[List[float]]) -> float:
    """Works in O(n^2), hight correlation with similar sentences length"""
    grade = 0
    for other_sentence in all_sentences:
        grade += get_cos_distance(sentence, other_sentence)
    return grade


def summarize(text: str):
    sentences = tools.split_to_sentences(text)
    lemmas_matrix = tools.get_lemmatized_matrix(text)
    vectorized_sentences = [
        make_avg_vector([get_word_vector(word) for word in sentence]) for sentence in lemmas_matrix
    ]
    total_vector = [0.0] * len(vectorized_sentences[0])
    for vc in vectorized_sentences:
        for i, vci in enumerate(vc):
            total_vector[i] += vci
    # choice one of grade functions
    index_with_grade = [
        (
            i,
            # get_grade_fast(counter, total_counter, total_words)
            get_grade_slow(sentence_vc, vectorized_sentences),
        )
        for i, sentence_vc in enumerate(vectorized_sentences)
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
