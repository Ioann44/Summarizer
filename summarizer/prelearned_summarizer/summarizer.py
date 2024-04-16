import os
import sys
from typing import List, Tuple, Iterable

from gensim.models import Word2Vec
from tqdm import tqdm

location = os.path.dirname(__file__)
sys.path.append(location + "/../")

import tools

model = Word2Vec.load(location + "/models/cbow_v300_slow.bin")


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
    i: int, all_sentences: List[List[float]], window_size=25
) -> Iterable[List[float]]:
    """Makes check window smaller to avoid O(n^2) and move to O(n) with large multiplier (window_size)

    Args:
        i (_type_): Index of grading vectorized sentence
        all_sentences (_type_): Array of others vectorized sentences
    """
    right = min(len(all_sentences), i + window_size // 2)
    left = max(0, right - window_size)
    right = min(len(all_sentences), left + window_size)
    vc_sent_generator = (all_sentences[j] for j in range(left, right) if j != i)
    return vc_sent_generator


def __summarize(lemmas_matrix: List[List[str]]) -> List[int]:
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
            (get_grade_slow(sentence_vc, get_beside_sentences_window(i, vectorized_sentences))),
        )
        for i, sentence_vc in tqdm(
            enumerate(vectorized_sentences), "Grading...", len(vectorized_sentences), ncols=100
        )
    ]
    index_with_grade.sort(key=lambda i_grade: -i_grade[1])

    summarized_indexes = [index for index, _ in index_with_grade]
    return summarized_indexes


def summarize_extended(text: str) -> List[Tuple[str, int]]:
    """Cover with additional info about summarizing

    Args:
        text (str): Source text

    Returns:
        List[Tuple[str, int]]: [(sentence, index of sentence in source text), ...]
    """
    sentences = tools.split_to_sentences(text)
    # lemmas_matrix = [tools.get_lemmatized_matrix_from_sentence(sentence) for sentence in sentences]
    lemmas_matrix = [
        tools.get_lemmatized_matrix_from_sentence(sentence)
        for sentence in tqdm(sentences, "Lemmatizing...", ncols=100)
    ]

    summarized_indexes = __summarize(lemmas_matrix)
    return [(sentences[i], i) for i in summarized_indexes]
