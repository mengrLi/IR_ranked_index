# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    :LossyCompression.py
# @Description: lossy compression include remove punctuation, remove number, remove special characters and stop words
# @Software: PyCharm
# @Author  : Mengran Li
# @Time    : 2019/10/31
# @Version : 1.0
import os
import re
from string import punctuation


def clean_num_character(str):
    return re.sub('[0-9’!#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+', "", str)


def clean_empty(str):
    return re.sub("[^A-Za-z0-9]", " ", str)


def normalized(tokens):
    text = tokens
    text = [token for token in text if not token in punctuation]
    text = filter(None, text)
    text = [token for token in text if not token == "''" and not token == '``']
    text = [token for token in text if not token == "\x03" and not token == "\x7f"]
    text = [token for token in text if not token.isdigit()]
    text = [token.lower() for token in text]
    stop_words = get_stopwords()
    text = [token for token in text if not token in stop_words]
    return text


def get_stopwords():
    stop_words = []
    if os.path.exists("stopwords.txt"):
        with open("stopwords.txt") as f:
            for line in f:
                stop_words.append(line.strip())
    else:
        print("Can not find the stopwords")
    return stop_words
