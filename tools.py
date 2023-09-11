from typing import List
import re
import nltk

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


word_regex = re.compile(r'([а-яё0-9]+)')
def get_words_from_sentence(sentence: str) -> List[str]:
    words = word_regex.findall(sentence)
    return words