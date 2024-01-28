import os
import sys
import csv
import random
from tqdm import tqdm

location = os.path.dirname(__file__)
sys.path.append(location + "/../" * 2)

import tools


# with open(location + "/lenta-ru-news.csv", "r", encoding="utf-8") as input_file:
with open(location + "/lenta-sample.csv", "r", encoding="utf-8") as input_file:
    csv_reader = csv.reader(input_file)

    with open(location + "/formatted-dataset.txt", "w", encoding="utf-8") as output_file:
    # with open(location + "/formatted-sample.txt", "w", encoding="utf-8") as output_file:
        for line in tqdm(csv_reader, "Converting data", total=868645, ncols=100):
            if random.random() <= 1:
                output_file.writelines(
                    " ".join(tools.lemmatize(word) for word in tools.get_words_from_sentence(sentence)) + "\n"
                    for sentence in tools.split_to_sentences(line[2].lower())
                )
