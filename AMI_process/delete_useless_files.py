# -*- coding: utf-8 -*-


"""
Delete useless files according to './data/list.ami' as done
in "Unsupervised abstractive meeting summarization with
multi-sentence compression and budgeted sub- modular maximization"
to get train/valid/test
Finally we will get train:97 valid:20 test:20 (list.ami.train/eval/test)
"""
import codecs
import utils
import os
import shutil


def get_usefulfile_list(path):
    """
    Get useful files according to './data/list.ami'
    Get the same dataset as "Unsupervised abstractive meeting summarization with
    multi-sentence compression and budgeted sub- modular maximization"
    :param path: path to list.ami
    :return: list of useful file names
    """
    files = []
    with codecs.open(path, "r", "utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                files.append(line)
    assert len(files) == 137  # total number of train/valid/test same as above paper
    return files


def make_tgt_dir(dir_path):
    """
    create target dirs to save useful files according './data/list.ami'
    tgt:
        data/ami/
        data/ami/words/
        data/ami/topics/
    :param dir_path: data/ami
    :return: path of new words dir and path of new topics dir
    """
    current_path = utils.get_project_dir()  # get working dir
    tgt_path = os.path.join(current_path, dir_path)

    # delete first
    if os.path.exists(tgt_path):
        shutil.rmtree(tgt_path)

    # make new dirs
    os.makedirs(tgt_path)
    os.makedirs(os.path.join(tgt_path, "words"))  # words sub dir (:ami_public_manual_1.6.2/words)
    os.makedirs(os.path.join(tgt_path, "topics"))  # topics sub dir (:ami_public_manual_1.6.2/topics)
    os.makedirs(os.path.join(tgt_path, "summary"))  # topics sub dir (:ami_public_manual_1.6.2/summary)

    return os.path.join(tgt_path, "words"), os.path.join(tgt_path, "topics"), os.path.join(tgt_path, "summary")


def filter_out_useless_files(useful_files, new_words_path, new_topics_path, new_summary_path):
    """
    Copy useful files to the new dir
    :param useful_files:
    :param new_words_path: path to the tgt words dir
    :param new_topics_path: path to the tgt topics dir
    :return:
    """

    # original data
    words_path = os.path.join(utils.get_project_dir(), "data/ami_public_manual_1.6.2/words")
    topics_path = os.path.join(utils.get_project_dir(), "data/ami_public_manual_1.6.2/topics")
    summary_path = os.path.join(utils.get_project_dir(), "data/ami_public_manual_1.6.2/abstractive")

    original_words_files = os.listdir(words_path)
    original_topics_files = os.listdir(topics_path)
    original_summary_files = os.listdir(summary_path)

    # copy words files
    for item in original_words_files:
        names = item.split(".")
        assert len(names) == 4
        id = names[0]
        if id in useful_files:
            cmd = "cp {} {}".format(os.path.join(words_path, item), new_words_path)
            os.system(cmd)

    # copy topics files
    for item in original_topics_files:
        names = item.split(".")
        assert len(names) == 3, item
        id = names[0]
        if id in useful_files:
            cmd = "cp {} {}".format(os.path.join(topics_path, item), new_topics_path)
            os.system(cmd)

    # copy summary files
    for item in original_summary_files:
        names = item.split(".")
        assert len(names) == 3, item
        id = names[0]
        if id in useful_files:
            cmd = "cp {} {}".format(os.path.join(summary_path, item), new_summary_path)
            os.system(cmd)


if __name__ == "__main__":
    new_words_path, new_topics_path, new_summary_path = make_tgt_dir("data/ami/")
    useful_files = get_usefulfile_list("./data/list.ami")
    filter_out_useless_files(useful_files, new_words_path, new_topics_path, new_summary_path)
