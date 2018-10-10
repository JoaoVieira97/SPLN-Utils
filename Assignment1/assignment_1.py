#!/usr/bin/env python3

# Assignment 1 - Remove Accentuation

import re
import sys

# List of possible accentuations for each vogal
a_accent = r'[àáãâ]'
e_accent = r'[éèê]'
i_accent = r'[íìî]'
o_accent = r'[óòôõ]'
u_accent = r'[úùû]'

replacement = {
		'a':a_accent,
		'e':e_accent,
		'i':i_accent,
		'o':o_accent,
		'u':u_accent	
	}

def remove_accents(text):
	text = re.sub(replacement['a'], 'a', text)
	text = re.sub(replacement['e'], 'e', text)
	text = re.sub(replacement['i'], 'i', text)
	text = re.sub(replacement['o'], 'o', text)
	text = re.sub(replacement['u'], 'u', text)
	return text

if(len(sys.argv)<=1):
	inp = input();
	print(remove_accents(inp))
else:
	for file in sys.argv[1:]:
		f = open(file, 'r')
		print("------------ " + file + " ------------ ") 
		print(remove_accents(f.read()))