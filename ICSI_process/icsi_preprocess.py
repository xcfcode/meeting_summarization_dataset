# -*- coding: utf-8 -*-

"""
Read speaker and utterances from *.da files.
Then clean utterances
"""
from utils import get_train_valid_test_files, clean_utterance
import codecs
import os


def create_stop_words():
    stop_words = []
    with codecs.open("data/stop_words.txt", 'r', "utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                stop_words.append(line)
    return stop_words


def process(files, mode, stop_words):
    for file in files:
        utterances = []
        f = codecs.open("./data/acl18-icsi/{}.da".format(file))
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split("\t")
                speaker = parts[3]
                utterance = parts[-1]

                utterance = clean_utterance(utterance, stop_words)  # clean utterances

                if utterance is not "" and len(utterance.split()) > 3:
                    utterances.append((speaker, utterance))

        with codecs.open("data/cleaned/{}/{}.txt".format(mode, file), "w", "utf-8") as w_f:
            for utterance in utterances:
                w_f.write(utterance[0])  # speaker
                w_f.write("\t")
                w_f.write(utterance[1])  # utterance
                w_f.write("\n")


if __name__ == "__main__":
    train_files, valid_files, test_files = get_train_valid_test_files("data/list.icsi.train", "data/list.icsi.eval",
                                                                      "data/list.icsi.test")

    os.makedirs("data/cleaned")
    os.makedirs("data/cleaned/train")
    os.makedirs("data/cleaned/valid")
    os.makedirs("data/cleaned/test")

    stop_words = create_stop_words()  # get stop words

    process(train_files, "train", stop_words)
    process(valid_files, "valid", stop_words)
    process(test_files, "test", stop_words)