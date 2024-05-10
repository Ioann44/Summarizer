from typing import Iterable, List, Tuple
import re, os

import nltk

if "INSIDE_DOCKER" not in os.environ:
    nltk.download("punkt")


# get lemmatize function
def init_pymorphy():
    import pymorphy2

    morph = pymorphy2.MorphAnalyzer()
    return lambda word: morph.parse(word)[0].normal_form  # type: ignore


lemmatize = init_pymorphy()


# specify split to sentences function
def split_to_sentences(text: str) -> List[str]:
    sentences = nltk.sent_tokenize(text)
    return sentences


word_regex = re.compile(r"([а-яё0-9]+)")
word_regex_with_capits = re.compile(r"([а-яёА-ЯЁ]+)")


def get_words_from_sentence(sentence: str) -> List[str]:
    words = word_regex.findall(sentence)
    return words


def get_lemmatized_matrix(text: str) -> List[List[str]]:
    return [get_lemmatized_matrix_from_sentence(sentence) for sentence in split_to_sentences(text.lower())]


def get_lemmatized_matrix_from_sentence(sentence: str) -> List[str]:
    return [lemmatize(word) for word in get_words_from_sentence(sentence)]


def get_words(text: str) -> Iterable[str]:
    matches = word_regex_with_capits.finditer(text)
    # pos_word_list = [(m.start(), m.end(), m.group(1)) for m in matches]
    return (m.group(1) for m in matches)