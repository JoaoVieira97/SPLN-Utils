#!/usr/bin/env python3

from bs4 import BeautifulSoup
from collections import defaultdict, Counter
import requests
import pickle
import sys, getopt, re


rss_url = "https://blog.filippo.io/rss/"

def refreshDB():
    updated_feed = requests.get(rss_url).content
    parse_tree = BeautifulSoup(updated_feed, "xml")
    news = parse_tree.find_all("item")
    for new in news:
        title = new.find('title').text
        print(title + '\n')

def procRequest(search_query):
    indexer = open("indexer", "rb")
    doc_index = pickle.load(indexer)
    tot_docs = len(doc_index)
    doc_scale = {}
    search_query = re.split(r'\s+', search_query)
    for term in search_query:
        doc_term = {}
        for doc in doc_index:
            if term in doc_index[doc]:
                doc_term[doc] = doc_index[doc][term]
        idf = len(doc_term)/tot_docs
        for doc in doc_term:
            doc_scale[doc] = doc_scale.get(doc, 0) + idf*doc_term[doc]
    relevant_docs = sorted(doc_scale.keys(), key=doc_scale.get, reverse=True)
    print(relevant_docs) #Most relevant document (titles)

def main():
    args, remainder = getopt.getopt(sys.argv[1:], "r")
    args = dict(args)
    if "-r" in args:
        refreshDB()
    else:
        procRequest()


if __name__ == "__main__":
    main()