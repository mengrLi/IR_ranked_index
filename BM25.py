#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : BM25.py
# @Description:
# @Software: PyCharm
# @Author  : Mengran Li
# @Time    : 2019/10/31
# @Version : 1.0
import json
import math
import os
import time

from bs4 import BeautifulSoup
from LossyCompression import clean_empty, clean_num_character, normalized
import nltk
from Parameters import Document, Term

# total document number
document_number = 0
# total document length
nonpositonal_dict = {}
dict = {}
document_length = 0
average_document_length = 0


class BM25:
    # This method is to read files in folder and seperate articles according to block size limitation
    def readFiles(self):
        folder = os.path.exists("reuters21578")
        BASEPATH = "reuters21578/"
        global dict

        if not folder:
            print("********NO SUCH FOLDER CAN BE FOUND********")

        else:
            files = os.listdir("reuters21578")
            files = sorted(files)
            for item in files:
                if item.endswith(".sgm"):
                    print(item)
                    stream = open(BASEPATH + item, encoding="latin-1")
                    content = stream.read()
                    soup_content = BeautifulSoup(content, "html.parser")
                    articles = soup_content.find_all('reuters')
                    block = self.separateArticles(articles)
                    for item in block.keys():
                        dict[item] = block[item]
        global document_number
        document_number = len(dict)
        self.process_documents(dict)

    # This method is to match article pattern and extract articles with ID from raw data
    def separateArticles(self, articles):
        block = {}
        for a in articles:
            body = ""
            title = ""
            newID = a['newid']
            if not a.title is None:
                title = a.title.string
            if not a.body is None:
                body = a.body.string
            text = title + " " + body
            doc = Document(newID, text)
            block[newID] = doc
        return block

    def process_documents(self, dictionary):
        global nonpositional_dict, document_length, average_document_length
        print("==== create index...====")
        start = time.time()
        for key in dictionary:
            doc = dictionary[key]
            text = clean_empty(doc.content)
            text = clean_num_character(text)
            tokens = nltk.word_tokenize(text)
            doc.doc_length = len(tokens)
            tokens = normalized(tokens)
            doc.tokens = tokens
            document_length = document_length + doc.doc_length
            # term frequency
            for token in tokens:
                if token not in doc.tf:
                    doc.tf[token] = 1
                else:
                    doc.tf[token] = doc.tf[token] + 1
            # document frequency
            for term in doc.tf:
                if term not in nonpositonal_dict:
                    nonpositonal_dict[term] = Term(t)
                nonpositonal_dict[term].create_posting_list(doc.id)
        end = time.time()
        print("time for creating index:" + str(end - start))
        print("total document length is:" + str(document_length))
        print("total document number is:" + str(document_number))
        average_document_length = document_length / document_number
        print("average document length is:" + str(average_document_length))

    def search(self, query):
        query_list = []
        tokens = nltk.word_tokenize(query)
        clean_queries = normalized(tokens)
        for token in clean_queries:
            query_list.append(token)
        if len(query_list) == 0:
            print("=====invalid input, try again====")
        self.get_score(query_list)

    def get_score(self, query_list):
        print(query_list)
        document_list = []
        k = 2
        b = 0.75

        global dict, document_number, nonpositonal_dict, average_document_length

        for item in query_list:
            if item in nonpositonal_dict.keys():
                posting_list = nonpositonal_dict[item].posting_list
                for i in posting_list:
                    if i not in document_list:
                        document_list.append(i)
        print(document_list)
        print("There are " + str(len(document_list)) + " relevant documents found!")
        print("Here, k = " + str(k) + " , b = " + str(b))
        score_dict = {}
        for item in document_list:
            document_score = 0

            doc = dict[item]
            for query in query_list:
                if query in doc.tokens:
                    idf = math.log(document_number / nonpositonal_dict[query].df, 10)

                    tf_td = doc.tf[query]
                    numerator = (k + 1) * tf_td
                    demominator = k * ((1 - b) + b * (doc.doc_length / average_document_length)) + tf_td
                    result = numerator / demominator
                    score = idf * result
                    document_score = document_score + score
                else:
                    document_score = document_score + 0

            score_dict[item] = document_score

        rank_result = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)
        print("ranked result is: " + str(rank_result))
        self.output_to_file(rank_result, query_list[0])

    def output_to_file(self, rank_result, name):
        path = "RESULT/"
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
        file_name = os.path.join(path, name + ".txt")
        jsonString = json.dumps(rank_result, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
        fo = open(file_name, "w")
        fo.write(jsonString)
        fo.close()

    def main(self):
        print("==== read files...====")
        self.readFiles()
        while (True):
            print("======== choose your command =======")
            print("=============1. search  ============")
            print("=============2. quit  ==============")
            order = int(input())
            if order == 1:
                print("====== please input the query ======")
                query = str(input())
                if query == "":
                    print("============= empty query ==============")
                    continue
                else:
                    self.search(query)
            elif order == 2:
                break
            else:
                print("============= invalid input ==============")


if __name__ == "__main__":
    t = BM25()
    t.main()
