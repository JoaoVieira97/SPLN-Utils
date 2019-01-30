#!/usr/bin/env python3

from bs4 import BeautifulSoup
from collections import defaultdict, Counter
import requests
import pickle
import sys, getopt
import regex as re

rss_url = "https://blog.filippo.io/rss/"

doc_index = {}

def refreshDB():
    updated_feed = requests.get(rss_url).content
    parse_tree = BeautifulSoup(updated_feed, "xml")
    news = parse_tree.find_all("item")
    links = [new.find("link").text for new in news]
    #for link in links:
    procNew(links[0])

def procNew(link):
    soup = BeautifulSoup(requests.get(link).text, "html.parser")
    title = soup.find('h1').text
    text = soup.find('main','content').find_all('p')
    buildDocIndex(text)
    filename = re.sub(r'\p{punct}', r'', title)
    filename = re.sub(r'\s+', r'_', filename)
    filename = filename.lower() + '.md'

    f = open(filename,'w')
    
    text = soup.find('main','content')
    find = text.find_all(["p", "pre", "h1", "h2", "h3"])
    for tag in find:
        if tag.name == 'h1':
            f.write('# ' + replaceToMd(str(tag)) + '\n')
        elif tag.name == 'h2':
            f.write('## ' + replaceToMd(str(tag)) + '\n')
        elif tag.name == 'h3':
            f.write('### ' + replaceToMd(str(tag)) + '\n')
        elif tag.name == 'p':
            f.write(replaceToMd(str(tag)) + '\n')
        elif tag.name == 'pre':
            f.write('```\n' + tag.text + '```\n')

def replaceToMd(html):
    html = re.sub(r'<strong>([^<]+)</strong>', r'__\1__', html) # important text
    html = re.sub(r'<b>([^<]+)</b>', r'__\1__', html) # bold text
    html = re.sub(r'<i>([^<]+)</i>', r'*\1*', html) # italic text
    html = re.sub(r'<em>([^<]+)</em>', r'*\1*', html) # emph text
    html = re.sub(r'<a href="([^"]+)">([^<]+)</a>', r'[\2](\1)', html) # references
    html = re.sub(r'<code>([^<]+)</code>', r'`\1`', html) # little code
    return BeautifulSoup(html, "html.parser").text

def buildDocIndex(text):
    pass

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