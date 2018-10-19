#!/usr/bin/env python3
#coding=utf8

""" Convert text to ASCII.

Write a program that reads unicode text as input and converts
it to ASCII text, removing accents and other non-ASCII characters,
keep the case.
"""
import sys
import re

def remove_accents(text):
	res=""

	for char in text:
		for regex in replacement:
			if(re.match(regex, char)):
				if(char.isupper()):
					char=replacement[regex][1]
				else:
					char=replacement[regex][0]
				break
		res+=char
	return res

if __name__=="__main__":
	a_accent = r'[àáãâÀÁÃÂ]'
	e_accent = r'[éèêÉÈÊ]'
	i_accent = r'[íìîÍÌÎ]'
	o_accent = r'[óòôõÓÒÔÕ]'
	u_accent = r'[úùûÚÙÛ]'

	replacement = {
		a_accent:'aA',
		e_accent:'eE',
		i_accent:'iI',
		o_accent:'oO',
		u_accent:'uU'	
	}

	if(len(sys.argv)<=1):
		inp = input();
		print(remove_accents(inp))
	else:
		for file in sys.argv[1:]:
			f = open(file, 'r')
			print("------------ " + file + " ------------ ")
			line = f.readline()
			while(len(line) > 0):
				print(remove_accents(line))
				line=f.readline()

__author__ = "Joao Vieira and Miguel Quaresma"