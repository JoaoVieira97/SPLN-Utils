#!/usr/bin/env python3
import sys
import os
import getopt
import expresso
import publico
import latex_utils
import fileinput
import re

def print_usage(util_name):
    print("USAGE\n")
    print(util_name + " [-ephi] [search_term ...]\n\n")
    print("DESCRIPTION\n")
    print("-p \t Search for news in Publico")
    print("-e \t Search for news in Expresso (not implemented)")
    print("-h \t Print this menu")
    print("-i \t Interactive mode")

def interactive_usage():
    print("\n\nUsage")
    print("p [search_term ....] : search for news in Publico")
    print("e [search_term ....] : search for news in Expresso (not implemented)")
    print("q : quit")
    print("h or help : print this menu\n\n")

def scrape(terms, newspaper):
    for argument in terms:
        newspaper_topic = newspaper + "_" + '-'.join(argument.split(' '))
        f_descriptor = open("noticias_"+ newspaper_topic + ".tex", "w")
        latex_utils.iniciarLatex(f_descriptor)
        if(newspaper == "expresso"):
            raise("Not implemented!")
            #expresso.pesquisarNoticias(argument, f_descriptor)
        else:
            publico.pesquisarNoticias(argument, f_descriptor)
        f_descriptor.write("\n\\end{document}")
        f_descriptor.close()
        os.system("pdflatex noticias_" + newspaper_topic + ".tex > /dev/null")
        print("Notícias do " + newspaper + " sobre " + argument + " podem ser encontradas no documento noticias_" + newspaper_topic + ".pdf")

def interactive_mode():
    interactive_usage()

    line = ""
    while line != "q":
        line = input()
        if line in ["h", "help"]:
            interactive_usage()
        elif line == "q":
            pass
        else:
            terms = re.findall(r'\'([^\']*)\'', line)
            line = line.split(' ')
            if not terms:
                if line[0] == "e":
                    scrape(line[1:], "expresso")
                elif line[0] == "p":
                    scrape(line[1:], "publico")
                else:
                    print("Invalid command! Enter h for usage")
            else:
                if line[0] == "e":
                    scrape(terms, "expresso")
                elif line[0] == "p":
                    scrape(terms, "publico")
                else:
                    print("Invalid command! Enter h for usage")

def main():
    args, remainder = getopt.getopt(sys.argv[1:], "ehip")
    args = dict(args)
    if "-h" in args:
        print_usage(sys.argv[0])
    if "-p" in args:
        scrape(remainder, "Público")
    if "-e" in args:
        scrape(remainder, "expresso")
    if "-i" in args:
        interactive_mode()

if __name__ == "__main__":
    main()
