############################################################
# Script for converting the base SRL data to CoNLL-like format for training purposes with various architectures.

# Pre-requisites: - 

# Usage : python srl2conll.py [path-to-SRL-file-for-Sumerian] [output-file-path]
############################################################

import os, sys
import codecs


INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

docs  = [] # Here we will store the outputs line-by-line

with codecs.open(INPUT_FILE, 'r', encoding='utf-8') as f, codecs.open(OUTPUT_FILE, 'w+', encoding='utf-8') as g:
	for line in f:
		if line.strip() == '':
			docs.append('\n')
			continue
		line  = line.strip().split('\t') #line-split with tab
		line.insert(2,'-')
		line.insert(2,'-')
		line.insert(2,'-')
		line.insert(2,'-')
		line.insert(2,'-')
		line.insert(2,'-')

		if line[8] !='Y':
			line[8] = '-'
		del line[9]

		print (line)
		line = '\t'.join(line)
		line = line.strip()
		print (line)
		docs.append(line)
		docs.append('\n')

	for item in docs:
		g.write(item)
