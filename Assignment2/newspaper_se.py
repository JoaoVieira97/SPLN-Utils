#!/usr/bin/env python3
import sys
import getopt
import publico

def print_usage(util_name):
    print("USAGE\n")
    print(util_name + " [-phi] [search_term ...]\n\n")
    print("DESCRIPTION\n")
    print("-p \t Search for news in Publico")
    print("-h \t Print usage/help")
    print("-i \t Interactive mode")

def main():
    args, remainder = getopt.getopt(sys.argv[1:], "hp")
    args = dict(args)
    if "-h" in args:
        print_usage(sys.argv[0])
    if "-p" in args:
        publico.scrape(remainder)

if __name__=="__main__":
    main()
