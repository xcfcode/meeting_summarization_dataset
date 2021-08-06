# -*- coding: utf-8 -*-

import codecs
import os

import utils

if __name__ == "__main__":
    _, _, test_files = utils.get_train_valid_test_files("data/list.icsi.train",
                                                        "data/list.icsi.eval",
                                                        "data/list.icsi.test")

    os.makedirs("./data/reference")

    o1 = codecs.open("./data/reference/ref1.txt", "w", "utf-8")
    o2 = codecs.open("./data/reference/ref2.txt", "w", "utf-8")
    o3 = codecs.open("./data/reference/ref3.txt", "w", "utf-8")

    for file in test_files:
        f1 = codecs.open("./data/summary/test/{}_summary_0.txt".format(file))
        f2 = codecs.open("./data/summary/test/{}_summary_1.txt".format(file))
        f3 = codecs.open("./data/summary/test/{}_summary_2.txt".format(file))

        o1.write(f1.readline() + "\n")
        o2.write(f2.readline() + "\n")
        o3.write(f3.readline() + "\n")

    f1.close()
    f2.close()
    f3.close()
    o1.close()
    o2.close()
    o3.close()
