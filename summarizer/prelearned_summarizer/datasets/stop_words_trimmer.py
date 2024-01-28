import os
import pickle
from collections import Counter

from tqdm import tqdm
import nltk

nltk.download("stopwords")
from nltk.corpus import stopwords

LOCATION = os.path.dirname(__file__) + "/"
NUM_LINES = 8879642

WORDS_CNT = 899619


def count_words():
    with open(LOCATION + "united.txt", encoding="utf-8") as fileIn:
        cnt = Counter()
        words_cnt = 0
        for i, line in tqdm(enumerate(fileIn), total=NUM_LINES, ncols=80):
            words = line.split()
            cnt += Counter(words)
            words_cnt += len(words)
            # limitation because of too large dataset
            if i > 50000:
                break
    print(words_cnt)
    with open(LOCATION + "counter.pkl", "wb") as fileOut:
        pickle.dump(cnt, fileOut)


def load_counter():
    with open(LOCATION + "counter.pkl", "rb") as fileIn:
        cnt: Counter = pickle.load(fileIn, encoding="utf-8")
    mostCmn = cnt.most_common(100)
    for i, item in enumerate(mostCmn):
        mostCmn[i] = (item[0], f"{item[1] / WORDS_CNT:%}")  # type: ignore
    pass


def trim():
    stops_set = set(stopwords.words("russian"))
    with open(LOCATION + "united.txt", encoding="utf-8") as fileIn:
        with open(LOCATION + "trimmed.txt", "w", encoding="utf-8") as fileOut:
            for line in tqdm(fileIn, total=NUM_LINES, ncols=80):
                res_list = []
                words = line.split()
                for word in words:
                    if word.isdigit() or word.replace("ё", "е") in stops_set:
                        continue
                    res_list.append(word)
                if res_list:
                    fileOut.write(" ".join(res_list) + "\n")


if __name__ == "__main__":
    # count_words()
    # load_counter()
    trim()