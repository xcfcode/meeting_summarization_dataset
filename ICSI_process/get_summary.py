# -*- coding: utf-8 -*-

import codecs
import os
import string

from utils import get_train_valid_test_files

punctuations = string.punctuation
import re


def get_summary_for_test(files):
    for file in files:
        for idx, key in enumerate(['beata', 's9553330', 'vkaraisk']):
            i = open("data/acl18-icsi/" + file + '.ducref.' + key + '.longabstract', 'r')
            o = open("data/summary/test/" + file + '_summary_' + str(idx) + '.txt', 'w')

            content = ''.join(l for l in i.read() if l not in punctuations)
            content = re.sub(' +', ' ', content)
            content = content.lower()
            content = content.replace("\n", " ")
            o.write(content)

            i.close()
            o.close()


def get_summary(files):
    for file in files:
        os.system("cp data/acl18-icsi/{}.ducref.longabstract data/summary/{}_summary.txt".format(file, file))


if __name__ == "__main__":
    train_files, valid_files, test_files = get_train_valid_test_files("data/list.icsi.train", "data/list.icsi.eval",
                                                                      "data/list.icsi.test")
    os.makedirs("data/summary")
    os.makedirs("data/summary/test")

    get_summary_for_test(test_files)
    get_summary(train_files)
    get_summary(valid_files)
