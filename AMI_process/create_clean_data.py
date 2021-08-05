# -*- coding: utf-8 -*-

import codecs

import os
import utils

CONST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z']


def create_stop_words():
    stop_words = []
    with codecs.open(os.path.join(utils.get_project_dir(), "data/ami/stop_words.txt"), 'r', "utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                stop_words.append(line)
    return stop_words


def clean_data(files, stop_words, mode):
    for file in files:
        utterances = []
        input_f = codecs.open(os.path.join(utils.get_project_dir(), "data/ami/{}/{}.txt").format(mode, file), "r",
                              "utf-8")
        lines = input_f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                segs = line.split("\t")
                person = segs[0].strip()
                time = segs[1].strip()
                utterance = segs[2].strip()
                topic = segs[3].strip()
                utterance = clear_utterance(utterance, stop_words)

                # if len(utterance.split()) <= 3:
                #     print("-----")
                if utterance is not "" and len(utterance.split()) > 3:
                    utterances.append((person, time, utterance, topic))

        with codecs.open(os.path.join(utils.get_project_dir(), "data/ami/cleaned/{}/{}.txt".format(mode, file)),
                         "w",
                         "utf-8") as w_f:
            for utterance in utterances:
                w_f.write(utterance[0])  # people
                w_f.write("\t")
                w_f.write(str(utterance[1]))  # time
                w_f.write("\t")
                w_f.write(utterance[2])  # utterance
                w_f.write("\t")
                w_f.write(utterance[3])
                w_f.write("\n")


def clear_utterance(utterance, stop_words):
    """

    :param utterance:
    :param stop_words:
    :return:
    """
    utterance = utterance.lower()

    for stop_word in stop_words:
        stop_word = stop_word.strip()
        if utterance.find(stop_word) != -1 and len(stop_word.split()) == 2:
            utterance = utterance.replace(stop_word, "")

    cleaned = []
    words = utterance.split()
    for word in words:
        if word not in stop_words:
            cleaned.append(word)
    utterance = " ".join(cleaned)

    cleaned = []
    for word in utterance.split():
        word = word.strip()
        if word not in CONST:
            cleaned.append(word)

    flag = False
    for word in cleaned:

        if word != "," and word != "." and word != "?":
            flag = True
            break

    if flag:
        if cleaned[0] == "." or cleaned[0] == ",":
            cleaned = cleaned[1:]
        utterance = " ".join(cleaned)
    else:
        utterance = ""

    return utterance


if __name__ == "__main__":
    train_files, valid_files, test_files = utils.get_train_valid_test_files("./data/list.ami.train",
                                                                            "./data/list.ami.eval",
                                                                            "./data/list.ami.test")

    # make output dirs
    os.makedirs(os.path.join(utils.get_project_dir(), "data/ami/cleaned"))
    os.makedirs(os.path.join(utils.get_project_dir(), "data/ami/cleaned/train"))
    os.makedirs(os.path.join(utils.get_project_dir(), "data/ami/cleaned/valid"))
    os.makedirs(os.path.join(utils.get_project_dir(), "data/ami/cleaned/test"))

    stop_words = create_stop_words()  # get stop words
    clean_data(train_files, stop_words, "train")
    clean_data(valid_files, stop_words, "valid")
    clean_data(test_files, stop_words, "test")
