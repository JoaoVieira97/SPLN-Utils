#!/usr/bin/env python3

from bs4 import BeautifulSoup
from collections import defaultdict, Counter
import requests
import sys, getopt
import pickle

rss_url = "https://blog.filippo.io/rss/"

def refreshDB():
    updated_feed = requests.get(rss_url).content
    parse_tree = BeautifulSoup(updated_feed, "xml")
    news = parse_tree.find_all("item")
    links = [new.find("link").text for new in news]
    for link in links:
        procNew(link)

def procNew(link):
    soup = BeautifulSoup(requests.get(link).text, "html.parser")
    title = soup.find('h1')
    text = soup.find('main','content').find_all('p')

def main():
    args, remainder = getopt.getopt(sys.argv[1:], "r")
    args = dict(args)
    if "-r" in args:
        refreshDB()
    else:
        procRequest()

if __name__ == "__main__":
    main()