############################################################
# Script for creating words-aligned representation from labeled aligned data.

# Pre-requisites: - 

# Usage : python label_to_word.py [../inputs/processed-etcsl-sumerian/] [../inputs/processed-etcsl-eng/]
############################################################

import os, sys, codecs
from itertools import izip

ALIGNMENT_FILE = sys.argv[1]
DATA_FILE = sys.argv[2]

with codecs.open(ALIGNMENT_FILE,  mode='r', encoding='utf-8') as a, codecs.open(DATA_FILE, mode='r', encoding='utf-8') as d:
	line_no = 1
	for x, y in izip(a, d):
		
		left_label_dict = {}
		right_label_dict = {}
		alignment = {}

		x = x.strip()
		y = y.strip()

		print (x)
		print (y)

		x = x.split(' ')
		y = y.split(' ||| ')
		if len(y) > 2:
			continue
		left = y[0].split(' ')
		right = y[1].split(' ')

		for i, word in enumerate(left):
			left_label_dict[i] = word
		for i, word in enumerate(right):
			right_label_dict[i] = word

		print (line_no)
		print (left_label_dict)
		print (right_label_dict)
		for item in x:
			item = item.split('-')
			if (left_label_dict[int(item[0])] in alignment):
				try:
					alignment[left_label_dict[int(item[0])]].append(right_label_dict[int(item[1])])
				except:
					print (int(item[1]), int(item[0]))
					print (line_no)
			else:
				alignment[left_label_dict[int(item[0])]] = []
				alignment[left_label_dict[int(item[0])]].append(right_label_dict[int(item[1])])

		print alignment

		line_no+=1
		#print (x.encode('utf-8'), y.encode('utf-8'))
