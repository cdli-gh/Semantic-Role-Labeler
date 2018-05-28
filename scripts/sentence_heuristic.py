import os, re, sys

#Usage : python sentence_heuristic.py [path-to-eng-file] [path-to-parallel-sumerian_file]

eng_file = sys.argv[1]
sum_file = sys.argv[2]

with open(eng_file, 'r') as f, open(sum_file, 'r') as g:
	