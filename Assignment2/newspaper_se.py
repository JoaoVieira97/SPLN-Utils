#!/usr/bin/env python3
import sys
import os
import getopt
import expresso
import publico
import latex_utils

def print_usage(util_name):
    print("USAGE\n")
    print(util_name + " [-ephi] [search_term ...]\n\n")
    print("DESCRIPTION\n")
    print("-e \t Search for news in Expresso")
    print("-p \t Search for news in Publico")
    print("-h \t Print usage/help")
    print("-i \t Interactive mode")

def scrape(terms, newspaper):
    for argument in terms:
        newspaper_topic = newspaper + "_" + '-'.join(argument.split(' '))
        f_descriptor = open("noticias_"+ newspaper_topic + ".tex", "w")
        latex_utils.iniciarLatex(f_descriptor)
        if(newspaper == "Expresso"):
            expresso.pesquisarNoticias(argument, f_descriptor)
        else:
            publico.pesquisarNoticias(argument, f_descriptor)
        f_descriptor.write("\n\\end{document}")
        f_descriptor.close()
        os.system("pdflatex noticias_" + newspaper_topic + ".tex > /dev/null")
        print("Notícias do " + newspaper + " sobre " + argument + " podem ser encontradas no documento noticias_" + newspaper_topic + ".pdf")

def main():
    args, remainder = getopt.getopt(sys.argv[1:], "ehp")
    args = dict(args)
    if "-h" in args:
        print_usage(sys.argv[0])
    if "-p" in args:
        scrape(remainder, "Público")
    if "-e" in args:
        scrape(remainder, "Expresso")

if __name__ == "__main__":
    main()
