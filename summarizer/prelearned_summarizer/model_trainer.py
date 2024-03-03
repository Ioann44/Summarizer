import os
import sys
import time
from typing import List
from collections import Counter

from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec

location = os.path.dirname(__file__)
sys.path.append(location + "/../")

import tools


class MyDataset:
    path = "/datasets/"

    def __init__(self, filename):
        self.path += filename

    def __iter__(self):
        with open(location + self.path, "r", encoding="utf-8") as input_file:
            for line in input_file:
                yield line.split()


class TrainingProgressCallback(CallbackAny2Vec):
    def __init__(self):
        self.epoch = 1
        self.previous_epoch_time = time.time()

    def on_epoch_end(self, model):
        now = time.time()
        epoch_seconds = now - self.previous_epoch_time
        self.previous_epoch_time = now

        loss = model.get_latest_training_loss()
        model.running_training_loss = 0.0

        print(f"Эпоха {self.epoch:3}, Потери: {loss}, Время: {epoch_seconds:.2f} с")
        self.epoch += 1


def create_model(name, dataset: MyDataset | None = None):
    model = Word2Vec(
        # sentences=dataset,
        corpus_file=location + "/datasets/trimmed.txt",
        vector_size=300,
        window=7,
        alpha=0.1,  # default 0.025
        min_count=10,  # default 5
        sg=0,  # 0 для CBOW, 1 для Skip-gram
        epochs=100,
        compute_loss=True,
        callbacks=[TrainingProgressCallback()],
        workers=5,
    )
    model.save(location + "/models/" + name)
    return model


def uptrain(name, epochs, dataset: MyDataset, new_name="default"):
    model = Word2Vec.load(location + "/models/" + name)
    model.build_vocab(dataset)
    model.train(
        dataset,
        total_examples=model.corpus_count,
        epochs=epochs,
        compute_loss=True,
        callbacks=[TrainingProgressCallback()],
    )
    if new_name == "default":
        model.save(location + "/models/" + name[:-4] + "_upt.bin")
    else:
        model.save(location + "/models/" + new_name)
    return model


# word_vectors = model.wv
# vector = word_vectors["пример"]
# 23 57
# 00 05
# recommend 80 epochs in case 8 mins per epoch on google colab

if __name__ == "__main__":
    MODEL_NAME = "cbow_v300.bin"
    DATASET_NAME = "trimmed.txt"

    # dataset = MyDataset(DATASET_NAME)

    # create_model(MODEL_NAME, dataset)
    # create_model(MODEL_NAME)

    # uptrain(NAME, 60, dataset=DATASET)

    model = Word2Vec.load(location + "/models/" + MODEL_NAME)

    def print_similar(word_in):
        word = tools.lemmatize(word_in)
        if word in model.wv:
            similar_words = model.wv.most_similar(word, topn=5)
        else:
            similar_words = []
        print(f"{word_in} = {word}:", [sim_word for sim_word, _ in similar_words])

    for word_to_check in "панк жизнь земля президент путин семья вода россия ящер".split():
        print_similar(word_to_check)
