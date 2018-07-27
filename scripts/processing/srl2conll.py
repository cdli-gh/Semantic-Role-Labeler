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
	a=1
	for line in f:
		print ("LINE NO. : ", a)
		print ("length: ", len(line))

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

		# if a blank word is obtained
		if line[1] == '':
			line[1] = 'XXXXX'

		if len(line) <=9 and len(line) >=8 :
			print ("LINE : ", a, len(line))
		if len(line) >=9 :
			if line[8] !='Y':
				line[8] = '-'
				'''
				if len(line) >= 13:
					del line[12]
					del line [11]
					del line[10]
				elif len(line) >= 12:
					del line[11]
					del line[10]
				elif len(line) >= 11:
					del line[10]
				'''
		elif len(line) >=7:
			print ("LINE NO. : ", a)
			print ("length: ", len(line))
			line[8] = '-'


		del line[9]

		#print (line)
		line = '\t'.join(line)
		line = line.strip()
		#print (line)
		docs.append(line)
		docs.append('\n')
		a+=1

	for item in docs:
		g.write(item)
