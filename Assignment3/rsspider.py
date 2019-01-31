#!/usr/bin/env python3

from bs4 import BeautifulSoup
from collections import defaultdict, Counter
import requests
import pickle
import os, math
import regex as re

rss_url = "https://blog.filippo.io/rss/"
index_dump = "rsspider.index"
directory = ".files/"
base_url = "https://blog.filippo.io"

doc_index = {}

def refreshDB():
    updated_feed = requests.get(rss_url).content
    parse_tree = BeautifulSoup(updated_feed, "xml")
    news = parse_tree.find_all("item")
    links = [new.find("link").text for new in news]
    os.makedirs(directory, exist_ok=True)
    for link in links:
        procNew(link)
    index_db = open(index_dump, "wb")
    pickle.dump(doc_index, index_db)


def procNew(link):
    soup = BeautifulSoup(requests.get(link).text, "html.parser")
    title = soup.find('h1').text
    text = soup.find('section','post-content').find_all('p')
    text = ' '.join([par.text for par in text])
    filename = re.sub(r'\p{punct}', r'', title)
    filename = re.sub(r'\s+', r'_', filename)
    filename = filename.lower() + '.html'
    buildDocIndex(filename, text)
    f =  open(directory + filename,'w')
    
    title = soup.find('h1', 'post-title')
    header_template = '''<!DOCTYPE html>
        <html xmlns="http://www.w3.org/1999/xhtml" lang="" xml:lang="">
        <head>
        <meta charset="utf-8" />
        <meta name="generator" content="pandoc" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
        <title>''' + title.text + '''</title>
        <link rel="stylesheet" type="text/css" href="../default.css"/>
        </head>
        <body>'''
    textsection = soup.find('section','post-content')
    find = textsection.find_all(["p", "pre", "h2", "h3", "h4", "ul", "ol", "blockquote"], recursive=False)
    text = '\n'.join([searchImg(str(tag)) for tag in find])
    f.write(header_template + '\n' + str(title) + '\n' + text + '</body>\n</html>\n')
    f.close()

def searchImg(tag):
    tag = re.sub(r'(<img alt="[^"]+" src=")([^"]+"/>)', r'\1' + base_url + r'\2', tag)
    return tag

def buildDocIndex(filename, text):
    doc_index[filename] = {}
    text = re.sub(r'\p{punct}', r'', text)
    text = text.lower()
    terms = re.split(r'\s+', text)
    
    for term in terms:
        doc_index[filename][term] = doc_index[filename].get(term, 0) + 1
    
    for term in doc_index[filename]:
        doc_index[filename][term] = doc_index[filename][term] / len(terms)
    

def procRequest(search_terms):
    indexer = open(index_dump, "rb")
    doc_index = pickle.load(indexer)
    tot_docs = len(doc_index)
    doc_scale = {}
    for term in search_terms:
        doc_term = {}
        for doc in doc_index:
            if term in doc_index[doc]:
                doc_term[doc] = doc_index[doc][term]
        try:
            idf = math.log(tot_docs/len(doc_term))
        except ZeroDivisionError:
            idf = 0
        for doc in doc_term:
            doc_scale[doc] = doc_scale.get(doc, 0) + idf*doc_term[doc]
    relevant_docs = sorted(doc_scale.keys(), key=doc_scale.get, reverse=True)
    return relevant_docs
