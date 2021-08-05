# -*- coding: utf-8 -*-

import codecs
import os


def get_project_dir():
    """
    Get project path
    :return: current path
    """
    current_dir = os.path.abspath(os.path.dirname(__file__))
    return current_dir


def get_start_time(elem):
    return elem[2]


def get_file_names(path):
    names = []
    with codecs.open(path, "r", "utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                names.append(line)
    return names


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

    assert len(train_files) == 97
    assert len(valid_files) == 20
    assert len(test_files) == 20

    return train_files, valid_files, test_files
