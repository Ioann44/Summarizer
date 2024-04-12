from typing import List, Tuple
from collections import Counter

from tqdm import tqdm
import tools


def __get_list_of_counters(sentences: List[str]) -> List[Counter[int]]:
    suppresses_sentences: List[List[int]] = []
    word_max_id = 0
    suppressor = dict()
    for sentence in tqdm(sentences, "Making counters", ncols=80):
        lowered_sentence = sentence.lower()
        suppresses_sentences.append([])
        for word in tools.get_words_from_sentence(lowered_sentence):
            lemma = tools.lemmatize(word)
            if lemma not in suppressor:
                suppressor[lemma] = word_max_id
                word_max_id += 1
            suppresses_sentences[-1].append(suppressor[lemma])

    return [Counter(num_list) for num_list in suppresses_sentences]


# assert (
#     __get_list_of_counters(["Раз два 'три'", "раз, дВа, три!"]) == [Counter({0: 1, 1: 1, 2: 1})] * 2
# ), "Get_array_of_counters not working properly"


def get_grade_fast(sentence: Counter, total_counter: Counter, total_words) -> float:
    """Works in O(n), low correlation with similar sentences length"""
    grade = 0
    for word_key, word_count in sentence.items():
        grade += word_count * (total_counter[word_key] - word_count)
    grade /= max(1, sum(sentence.values()))
    return grade


# def get_grade_slow(sentence: Counter, counters: List[Counter]) -> float:
#     """Works in O(n^2), hight correlation with similar sentences length"""
#     grade = 0
#     sentence_len = sum(sentence.values())
#     for other_sentence in counters:
#         cur_grade = 0
#         for word_key, word_count in sentence.items():
#             cur_grade += word_count * other_sentence.get(word_key, 0)
#         cur_grade /= max(1, sentence_len + sum(other_sentence.values()))
#         grade += cur_grade
#     return grade


def summarize(text: str) -> List[Tuple[str, int]]:
    sentences = tools.split_to_sentences(text)
    counters = __get_list_of_counters(sentences)
    total_counter = Counter()
    total_words = 0
    for counter in counters:
        total_counter += counter
        total_words += sum(counter.values())
    # choice one of grade functions
    index_with_grade = [
        (
            i,
            get_grade_fast(counter, total_counter, total_words),
        )
        for i, counter in enumerate(counters)
    ]
    index_with_grade.sort(key=lambda i_grade: -i_grade[1])
    return [(sentences[i], i) for i, _ in index_with_grade]
