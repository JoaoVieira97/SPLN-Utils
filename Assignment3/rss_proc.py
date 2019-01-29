#!/usr/bin/env python3

from bs4 import BeautifulSoup
from collections import defaultdict, Counter
import requests
import sys, getopt
import pickle


rss_url = "https://blog.filippo.io/rss/"

def refreshDB():
    updated_feed = requests.get(rss_url).content
    parse_tree = BeautifulSoup(updated_feed, "lxml")
    news = parse_tree.find_all("item")
    #TODO: proc news

def procRequest():
    pass

def main():
    args, remainder = getopt.getopt(sys.argv[1:], "r")
    args = dict(args)
    if "-r" in args:
        refreshDB()
    else:
        procRequest()


if __name__ == "__main__":
    main()