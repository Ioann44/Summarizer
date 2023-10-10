import os
import sys
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
from typing import List
from collections import Counter

location = os.path.dirname(__file__)
sys.path.append(location + "/../")

import tools


class TrainingProgressCallback(CallbackAny2Vec):
    def __init__(self):
        self.prev_loss_total = 0
        self.epoch = 1

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        self.prev_loss_total, loss = loss, loss - self.prev_loss_total
        print("Эпоха #{}: Потери: {}".format(self.epoch, loss))
        self.epoch += 1


def create_model():
    with open(location + "/datasets/formatted-dataset.txt", "r", encoding="utf-8") as input_file:
        sentences = [line.split() for line in input_file.readlines()]

    model = Word2Vec(
        sentences=sentences,
        vector_size=100,
        window=5,
        min_count=1,
        sg=0,  # 0 для CBOW, 1 для Skip-gram
        epochs=100,
        compute_loss=True,
        callbacks=[TrainingProgressCallback()],
    )
    model.save(location + "/models/cbow.bin")
    return model


def uptrain(name, epochs, new_name="default"):
    model = Word2Vec.load(location + "/models/" + name)
    with open(location + "/datasets/formatted-dataset.txt", "r", encoding="utf-8") as input_file:
        sentences = [line.split() for line in input_file.readlines()]
    model.build_vocab(sentences)
    model.train(
        sentences,
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


if __name__ == "__main__":
    # create_model()
    # uptrain("cbow_large.bin", 60, "cbow_large.bin")

    model = Word2Vec.load(location + "/models/cbow_large.bin")
    # model = Word2Vec.load(location + "/models/cbow_100v_5w_100e.bin")

    def print_similar(word):
        if word in model.wv:
            similar_words = model.wv.most_similar(word, topn=5)
        else:
            similar_words = []
        print(f"{word}:", [sim_word for sim_word, _ in similar_words])

    for word_to_check in "панк жизнь земля президент путин семья вода россия ящер".split():
        print_similar(word_to_check)
