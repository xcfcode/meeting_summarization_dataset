# -*- coding: utf-8 -*-

import codecs
import re

CONST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z']


def get_train_valid_test_files(train_path, valid_path, test_path):
    train_files = []
    valid_files = []
    test_files = []

    with codecs.open(train_path, "r", "utf-8") as train_f:
        lines = train_f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                train_files.append(line)

    with codecs.open(valid_path, "r", "utf-8") as valid_f:
        lines = valid_f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                valid_files.append(line)

    with codecs.open(test_path, "r", "utf-8") as test_f:
        lines = test_f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                test_files.append(line)

    assert len(train_files) == 53
    assert len(valid_files) == 25
    assert len(test_files) == 6

    return train_files, valid_files, test_files


def clean_utterance_acl18(utt, stop_words):
    """
    this code is borrowed from ACL18 code https://bitbucket.org/dascim/acl2018_abssumm/src/master/data/utils.py
    :param utt: utterance
    :return:
    """
    for ch in ['{vocalsound}', '{gap}', '{disfmarker}', '{comment}', '{pause}', '@reject@']:
        utt = re.sub(ch, '', utt)

    utt = re.sub("'Kay", 'Okay', utt)
    utt = re.sub("'kay", 'Okay', utt)
    utt = re.sub('"Okay"', 'Okay', utt)
    utt = re.sub("'cause", 'cause', utt)
    utt = re.sub("'Cause", 'cause', utt)
    utt = re.sub('"cause"', 'cause', utt)
    utt = re.sub('"\'em"', 'them', utt)
    utt = re.sub('"\'til"', 'until', utt)
    utt = re.sub('"\'s"', 's', utt)

    # l. c. d. -> lcd
    # t. v. -> tv
    utt = re.sub('h. t. m. l.', 'html', utt)
    utt = re.sub(r"(\w)\. (\w)\. (\w)\.", r"\1\2\3", utt)
    utt = re.sub(r"(\w)\. (\w)\.", r"\1\2", utt)
    utt = re.sub(r"(\w)\.", r"\1", utt)

    def clean(utterance, filler_words):
        utt = utterance
        # replace consecutive unigrams with a single instance
        utt = re.sub('\\b(\\w+)\\s+\\1\\b', '\\1', utt)
        # same for bigrams
        utt = re.sub('(\\b.+?\\b)\\1\\b', '\\1', utt)
        # strip extra white space
        utt = re.sub(' +', ' ', utt)
        # strip leading and trailing white space
        utt = utt.strip()

        # remove filler words # highly time-consuming
        utt = ' ' + utt + ' '
        for filler_word in filler_words:
            utt = re.sub(' ' + filler_word + ' ', ' ', utt)
            utt = re.sub(' ' + filler_word.capitalize() + ' ', ' ', utt)

        return utt

    # clean_utterance, remove filler_words
    utt = clean(utt, filler_words=stop_words)

    # strip extra white space
    utt = re.sub(' +', ' ', utt)
    # strip leading and trailing white space
    utt = utt.strip()
    return utt


def clean_utterance(utterance, stop_words):
    """
    clean utterance
    :param utterance:
    :param stop_words:
    :return:
    """

    """ acl18 clean """
    utterance = clean_utterance_acl18(utterance, stop_words)

    """ my own clean """
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
