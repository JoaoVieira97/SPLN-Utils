#!/usr/bin/env python3

# Assignment 1 - Remove Accentuation

import re
import sys

# List of possible accentuations for each vogal
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

if(len(sys.argv)<=1):
	inp = input();
	print(remove_accents(inp))
else:
	for file in sys.argv[1:]:
		f = open(file, 'r')
		print("------------ " + file + " ------------ ")
		print(remove_accents(f.read()))