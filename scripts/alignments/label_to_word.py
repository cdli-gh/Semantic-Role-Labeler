############################################################
# Script for creating words-aligned representation from labeled aligned data.

# Pre-requisites: - 

# Usage : python label_to_word.py ../../outputs/word-alignments/efmaral-aligner/index-aligned/efmaral-symm.dat ../../processed-data/cdli/un-normalised/sum_eng_train_unnorm.csv 

############################################################

import os, sys, codecs
from itertools import izip

ALIGNMENT_FILE = sys.argv[1]
DATA_FILE = sys.argv[2]


with open(ALIGNMENT_FILE,  'r') as a, open(DATA_FILE, 'r') as d, open('efmaral-words-aligned-symm.dat', 'w+') as w:
	line_no = 1
	total_list = []
	for x, y in izip(a, d):
		
		left_label_dict = {}
		right_label_dict = {}
		alignment = {}

		x = x.strip()
		y = y.strip()

		#print (x)
		#print (y)

		#Error handling
		if len(x) == 0 or len(y) == 0:
			print "Empty"
			alignment['empty'] = 1
			

		x = x.split(' ')
		y = y.split(' ||| ')
		#if len(y) > 2:
		#	continue
		left = y[0].split(' ')
		right = y[1].split(' ')

		for i, word in enumerate(left):
			left_label_dict[i] = word
		for i, word in enumerate(right):
			right_label_dict[i] = word

		print (line_no)

		word_sentence = "" #This word list string is unique for each sentence.
		for item in x:
			item = item.split('-')
			try:
				word_sentence = word_sentence + left_label_dict[int(item[0])] + '|' + right_label_dict[int(item[1])] + ' '
			except:
				word_sentence += "Error "
		word_sentence = word_sentence.strip()
		total_list.append(word_sentence)
		line_no+=1

		'''
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

		temp_list = []
		for key, val in alignment.iteritems():
			val_str = ""
			for elem in val:
				val_str = val_str + elem + '|'

			temp_list.append(key + '--' + val_str)

		sentence_str = ""
		for item in temp_list:
			sentence_str += item
		total_list.append(sentence_str)
		line_no+=1
		#print (x.encode('utf-8'), y.encode('utf-8'))
		'''

	for item in total_list:
		w.write(item+'\n')
