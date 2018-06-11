############################################################
# Script for unnormalising Cdli-UrIII data.

# Pre-requisites: - 

# Usage : python unnormalise.py [path-to-file-to-unnormalise] [output-file-path.py]
############################################################

import os, sys
import codecs


INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

docs  = [] # Here we will store the outputs line-by-line

with codecs.open(INPUT_FILE, 'r', encoding='utf-8') as f, codecs.open(OUTPUT_FILE, 'w+', encoding='utf-8') as g:
	for line in f:
		
		line = line.replace(u"ordNUMB", "4")
		line = line.replace(u"NUMB", "3")
		docs.append(line)

	for item in docs:
		g.write(item)
