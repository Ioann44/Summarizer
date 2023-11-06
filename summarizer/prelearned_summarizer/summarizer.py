import itertools
import math
import os
import sys
from typing import List, Sized, Tuple, Iterable, Set

from gensim.models import Word2Vec
from tqdm import tqdm

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
    if len(vectors) == 0:
        return []
    total_vector = [0.0] * len(vectors[0])
    for vc in vectors:
        for i, vci in enumerate(vc):
            total_vector[i] += vci
    for i in range(len(total_vector)):
        total_vector[i] /= len(vectors)
    return total_vector


def get_cos_distance(vc_a: List[float], vc_b: List[float]) -> float:
    if not any(vc_a) or not any(vc_b):
        return 0
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


def get_grade_slow(sentence: List[float], all_sentences: Iterable[List[float]]) -> float:
    """Works in O(n^2), hight correlation with similar sentences length"""
    grade = 0
    for other_sentence in all_sentences:
        grade += get_cos_distance(sentence, other_sentence)
    return grade


def get_beside_sentences_window(
    i: int, all_sentences: List[List[float]], window_size=100
) -> Iterable[List[float]]:
    """Makes check window smaller to avoid O(n^2) and move to O(n) with large multiplier (window_size)

    Args:
        i (_type_): Index of grading vectorized sentence
        all_sentences (_type_): Array of others vectorized sentences
    """
    right = min(len(all_sentences), i + window_size // 2)
    left = max(0, right - 100)
    right = left + 100
    vc_sent_generator = itertools.islice(all_sentences, left, right)
    return vc_sent_generator


def get_rid_of_small_sentences(indexes: Iterable[int], sentences: List[Sized], min_len: int = 4) -> Set[int]:
    set_of_i = set()
    for i in indexes:
        if len(sentences[i]) >= min_len:
            set_of_i.add(i)
    return set_of_i


def __summarize(
    lemmas_matrix: List[List[str]], compression_multiplier: float, grade_method_is_slow: bool
) -> List[int]:
    vectorized_sentences = [
        # make_avg_vector([get_word_vector(word) for word in sentence]) for sentence in lemmas_matrix
        make_avg_vector([get_word_vector(word) for word in sentence])
        for sentence in tqdm(lemmas_matrix, "Vectorizing...", ncols=100)
    ]
    total_vector = [0.0] * len(vectorized_sentences[0])
    for vc in vectorized_sentences:
        for i, vci in enumerate(vc):
            total_vector[i] += vci

    index_with_grade = [
        (
            i,
            get_grade_slow(sentence_vc, get_beside_sentences_window(i, vectorized_sentences))
            if grade_method_is_slow
            else 1,
        )
        # for i, sentence_vc in enumerate(vectorized_sentences)
        for i, sentence_vc in tqdm(
            enumerate(vectorized_sentences), "Grading...", len(vectorized_sentences), ncols=100
        )
    ]
    index_with_grade.sort(key=lambda i_grade: i_grade[1])

    """better to rewrite next block to correlate with len of symbols in sentence instead of words,
    also move it to the top to exclude small sentences from grading (number may cause a lot of harm I think)"""
    inds_of_long_sentences = get_rid_of_small_sentences((i for i, _ in index_with_grade), lemmas_matrix)  # type: ignore
    # index of long enough sentences, plus grade
    iofes_with_grade = [(i, grade) for i, grade in index_with_grade if i in inds_of_long_sentences]

    summarized_index_with_grade = iofes_with_grade[: math.ceil(len(lemmas_matrix) / compression_multiplier)]
    summarized_index_with_grade.sort()
    return [index for index, grade in summarized_index_with_grade]


def summarize_extended(
    text: str, compression_multiplier: float = 3, is_slow_preferred: bool = True
) -> Tuple[str, int, int]:
    """Cover with additional info about summarizing

    Args:
        text (str): Source text
        compression_multiplier (float, optional): How many times sentences num will be decreased. Defaults to 3.
        is_slow_preferred (bool, optional): Which summarizing method preffered. Defaults to True.

    Returns:
        Tuple[str, int, int]: Summarized text, initial sentences num, compressed sentences num
    """
    sentences = tools.split_to_sentences(text)
    # lemmas_matrix = [tools.get_lemmatized_matrix_from_sentence(sentence) for sentence in sentences]
    lemmas_matrix = [
        tools.get_lemmatized_matrix_from_sentence(sentence)
        for sentence in tqdm(sentences, "Lemmatizing...", ncols=100)
    ]

    # add force using fast method if there are too many sentences
    summarized_indexes = __summarize(lemmas_matrix, compression_multiplier, is_slow_preferred)

    return " ".join(sentences[i] for i in summarized_indexes), len(sentences), len(summarized_indexes)


if __name__ == "__main__":
    with open(location + "/../../other/philosofy1m.txt", "r", encoding="utf-8") as file:
        # with open(location + "/../../other/input.txt", "r", encoding="utf-8") as file:
        input_text = file.read()
    res, initial_num, result_num = summarize_extended(input_text, 50)
    print(f"Compressed from {initial_num} to {result_num} sentences")
    with open(location + "/../../other/output.txt", "a", encoding="utf-8") as file:
        file.write("\n" * 2)
        file.write(res)
