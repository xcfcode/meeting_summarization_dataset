# -*- coding: utf-8 -*-

import codecs
from xml.dom import minidom

import os

import utils


def get_default_topics():
    """
    Get default topics from ami_public_manual_1.6.2/ontologies/default-topics.xml
    map default topic id to topic description
    :return: dict of default_topic
    """
    default_topic = {
        "default-topics.xml#id(top.1)": "Functional",
        "default-topics.xml#id(top.11)": "opening",
        "default-topics.xml#id(top.12)": "closing",
        "default-topics.xml#id(top.13)": "agenda/equipment issues",
        "default-topics.xml#id(top.14)": "chitchat",
        "default-topics.xml#id(top.2)": "Top level",
        "default-topics.xml#id(top.21)": "project specs and roles of participants",
        "default-topics.xml#id(top.22)": "new requirements",
        "default-topics.xml#id(top.23)": "user target group",
        "default-topics.xml#id(top.24)": "interface specialist presentation",
        "default-topics.xml#id(top.25)": "marketing expert presentation",
        "default-topics.xml#id(top.26)": "industrial designer presentation",
        "default-topics.xml#id(top.27)": "presentation of prototype(s)",
        "default-topics.xml#id(top.28)": "discussion",
        "default-topics.xml#id(top.29)": "evaluation of prototype(s)",
        "default-topics.xml#id(top.210)": "evaluation of project process",
        "default-topics.xml#id(top.211)": "costing",
        "default-topics.xml#id(top.212)": "drawing exercise",
        "default-topics.xml#id(top.3)": "Sub-topics",
        "default-topics.xml#id(top.31)": "project budget",
        "default-topics.xml#id(top.32)": "existing products",
        "default-topics.xml#id(top.33)": "trendwatching",
        "default-topics.xml#id(top.34)": "user requirements",
        "default-topics.xml#id(top.35)": "components, materials and energy sources",
        "default-topics.xml#id(top.36)": "look and usability",
        "default-topics.xml#id(top.37)": "how to find when misplaced"
    }
    return default_topic


def iterative_word2topic_map(topic_node, word2topic_mapping_dict, default_topic):
    """
    Create word2topic map for every node
    :param topic_node: node in doc
    :param word2topic_mapping_dict: current mapping dict
    :param default_topic: default topics
    :return:
    """
    # this means its child nodes all belong to this topic, does not be covered by default topics
    if topic_node.hasAttribute("other_description"):
        topic = topic_node.getAttribute('other_description')
    elif topic_node.hasAttribute("description"):
        topic = topic_node.getAttribute('description')

    # for its childs
    for node in topic_node.childNodes:
        if node.nodeType == node.ELEMENT_NODE:
            if node.nodeName == "nite:pointer":
                if node.getAttribute('href') == "default-topics.xml#id(top.4)":
                    # topic : description or other_description
                    pass
                else:
                    # default topics
                    topic = default_topic[node.getAttribute('href')]
            elif node.nodeName == "topic":
                # recursive create map
                word2topic_mapping_dict = iterative_word2topic_map(node, word2topic_mapping_dict, default_topic)
            elif node.nodeName == "nite:child":
                word_range = node.getAttribute(
                    'href')  # TS3009d.C.words.xml#id(TS3009d.C.words1655)..id(TS3009d.C.words1670)
                id_range = word_range.split("#")[1]  # id(TS3009d.C.words1655)..id(TS3009d.C.words1670)
                if ".." in id_range:
                    start2end = id_range.split("..")
                    start = start2end[0].replace("id", "").replace("(", "").replace(")", "")  # TS3009d.C.words1655
                    end = start2end[1].replace("id", "").replace("(", "").replace(")", "")  # TS3009d.C.words1670
                    prefix = start[0:15]  # or end[0:15] S3009d.C.words
                    start_id = int(start[15:])  # 1655
                    end_id = int(end[15:])  # 1670
                    for i in range(start_id, end_id + 1):
                        word2topic_mapping_dict[prefix + str(i)] = topic
                else:
                    start = id_range.replace("id", "").replace("(", "").replace(")", "")
                    word2topic_mapping_dict[start] = topic
    return word2topic_mapping_dict


def create_word2topic_map(topic_file_path, default_topic):
    """
    Using xxxxxxx.topic.xml to create single word to topic map {ES2002a.A.words0:topic}
    :param topic_file_path: which file to be preprocessed
    :param default_topic: default topic dict
    :return:
    """
    word2topic_mapping_dict = dict()  # final word2topic mapping dict
    topic_doc = minidom.parse(topic_file_path)  # parse the whole file
    nodes = topic_doc.getElementsByTagName("topic")  # get all child nodes for the whole doc (top level)
    for node in nodes:  # for every node, recursive create map
        word2topic_mapping_dict = iterative_word2topic_map(node, word2topic_mapping_dict, default_topic)

    return word2topic_mapping_dict


def get_utterance_for_onepeople(people, path, topic_mapping_dict):
    """
    get utterances for one person {ES2002a.A.words.xml}
    :param people: people
    :param paths: words file path
    :param topic_mapping_dict: word id --> topic
    :return:
    """
    utterances = []  # sequence of tuples

    # parse xml doc
    word_doc = minidom.parse(path)

    # init
    utterance_word_ids = []
    utterance = ""
    start_time = 0

    words = word_doc.getElementsByTagName('w')
    for word in words:
        if word.hasAttribute("starttime"):
            text = word.firstChild.data
            # if end with '.' or '?'. it will be an utterance
            seg = True if word.hasAttribute(
                'punc') and (text == "." or text == "?") else False
            if seg:
                utterance += text
                utterances.append(
                    (people, utterance, start_time, get_topics_for_utterance(utterance_word_ids, topic_mapping_dict)))
                # reset
                utterance = ""
                utterance_word_ids = []
                start_time = 0
            else:
                utterance += text
                utterance += " "
                utterance_word_ids.append(word.getAttribute("nite:id"))

                # when an new utterance start
                if start_time == 0:
                    start_time = float(word.getAttribute("starttime"))
        else:
            # some error datas
            print("word {} does not have start time, pass it!".format(word.getAttribute("nite:id")))
    return utterances


def get_topics_for_utterance(utterance_word_ids, topic_mapping_dict):
    """
    Get relevant topics for one utterance
    :param utterance_word_ids: sequence of word id
    :param topic_mapping_dict: word id --> topic
    :return:
    """
    topic_set = set()
    for word_id in utterance_word_ids:
        if topic_mapping_dict is not None:
            topic = topic_mapping_dict.get(word_id)
            if topic:  # if a word does not have a topic, topic will be none
                topic_set.add(topic)
        else:
            # ES2006c  ES2015b  ES2015c do not have topic files
            topic_set.add("NO_TOPIC")
    # set2list
    if len(topic_set) == 0:
        topic_set.add("NO_TOPIC")
    return list(topic_set)


if __name__ == "__main__":
    file_names = utils.get_file_names("./data/list.ami")
    default_topic_dict = get_default_topics()

    train_files, valid_files, test_files = utils.get_train_valid_test_files("./data/list.ami.train",
                                                                            "./data/list.ami.eval",
                                                                            "./data/list.ami.test")

    # first mkdir data/ami/train data/ami/valid data/ami/test
    os.makedirs(os.path.join(utils.get_project_dir(), "data/ami/train"))
    os.makedirs(os.path.join(utils.get_project_dir(), "data/ami/valid"))
    os.makedirs(os.path.join(utils.get_project_dir(), "data/ami/test"))

    for file_name in file_names:
        meeting_utterances = []
        topic_file_path = "./data/ami/topics/{}.topic.xml".format(file_name)

        if os.path.exists(topic_file_path):
            word2topic_mapping_dict = create_word2topic_map(topic_file_path, default_topic_dict)
        else:
            # ES2006c  ES2015b  ES2015c do not have topic files
            word2topic_mapping_dict = None

        # every meeting have four users ABCD
        A_utterances = get_utterance_for_onepeople("A", "./data/ami/words/{}.A.words.xml".format(file_name),
                                                   word2topic_mapping_dict)
        B_utterances = get_utterance_for_onepeople("B", "./data/ami/words/{}.B.words.xml".format(file_name),
                                                   word2topic_mapping_dict)
        C_utterances = get_utterance_for_onepeople("C", "./data/ami/words/{}.C.words.xml".format(file_name),
                                                   word2topic_mapping_dict)
        D_utterances = get_utterance_for_onepeople("D", "./data/ami/words/{}.D.words.xml".format(file_name),
                                                   word2topic_mapping_dict)
        meeting_utterances.extend(A_utterances)
        meeting_utterances.extend(B_utterances)
        meeting_utterances.extend(C_utterances)
        meeting_utterances.extend(D_utterances)

        # sort by start time
        meeting_utterances.sort(key=utils.get_start_time)

        if file_name in train_files:
            f = codecs.open(os.path.join(utils.get_project_dir(), "data/ami/train/{}.txt".format(file_name)), "w",
                            "utf-8")
        elif file_name in valid_files:
            f = codecs.open(os.path.join(utils.get_project_dir(), "data/ami/valid/{}.txt".format(file_name)), "w",
                            "utf-8")
        elif file_name in test_files:
            f = codecs.open(os.path.join(utils.get_project_dir(), "data/ami/test/{}.txt".format(file_name)), "w",
                            "utf-8")

        for utterance in meeting_utterances:
            f.write(utterance[0])  # people
            f.write("\t")
            f.write(str(utterance[2]))  # time
            f.write("\t")
            f.write(utterance[1])  # utterance
            f.write("\t")
            f.write(" ".join(utterance[3]))
            f.write("\n")

        f.close()
