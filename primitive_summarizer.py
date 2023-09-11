from typing import List
from collections import Counter
import tools


def __get_list_of_counters(sentences: List[str]) -> List[Counter[int]]:
    suppresses_sentences: List[List[int]] = []
    word_max_id = 0
    suppressor = dict()
    for sentence in sentences:
        lowered_sentence = sentence.lower()
        suppresses_sentences.append([])
        for word in tools.get_words_from_sentence(lowered_sentence):
            lemma = tools.lemmatize(word)
            if lemma not in suppressor:
                suppressor[lemma] = word_max_id
                word_max_id += 1
            suppresses_sentences[-1].append(suppressor[lemma])

    return [Counter(num_list) for num_list in suppresses_sentences]


assert (
    __get_list_of_counters(["Раз два 'три'", "раз, дВа, три!"]) == [Counter({0: 1, 1: 1, 2: 1})] * 2
), "Get_array_of_counters not working properly"


def summarize(text: str):
    sentences = tools.split_to_sentences(text)
    counters = __get_list_of_counters(sentences)
    total_counter = Counter()
    for counter in counters:
        total_counter += counter


if __name__ == "__main__":
    pass