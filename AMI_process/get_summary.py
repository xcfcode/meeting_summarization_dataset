# -*- coding: utf-8 -*-

import codecs
from xml.dom import minidom
import os

import utils

"""
Extract summary from xml files
mkdir data/ami/final_summary
python get_summary.py
"""


def get_summary_sentences(path):
    """
    get summary sentences from xml files
    :param path: xml file path
    :return:
    """
    summaries = []
    doc = minidom.parse(path)
    sentences = doc.getElementsByTagName('sentence')
    for sentence in sentences:
        if sentence.firstChild.data:
            summaries.append(sentence.firstChild.data)
    return summaries


def write_file(file_name, summary_list):
    """
    write summary sentences to txt file
    :param file_name:
    :param summary_list:
    :return:
    """
    with codecs.open(os.path.join(utils.get_project_dir(), "data/ami/final_summary/{}.txt".format(file_name)), "w",
                     "utf-8") as f:
        for sentence in summary_list:
            f.write(sentence)
            f.write("\n")


if __name__ == "__main__":
    file_names = utils.get_file_names("./data/list.ami")
    os.makedirs(os.path.join(utils.get_project_dir(), "data/ami/final_summary"))
    for file_name in file_names:
        summaries = get_summary_sentences(
            os.path.join(utils.get_project_dir(), "data/ami/summary/{}.abssumm.xml".format(file_name)))
        write_file(file_name, summaries)
