
# Usage : python sentence_segment.py [path-to-eng-ascii-ile] [path-to-parallel-sumerian_file] [output_eng_file] [output_sum_file]

import os, re, sys

eng_file = sys.argv[1]
sum_file = sys.argv[2]
OUTPUT_ENG_FILE = sys.argv[3]
OUTPUT_SUM_FILE = sys.argv[4]

file1= [] # Store Eng transformed file as list of sentences/.
file2= [] # Store Sumerian transformed file as a list of sentences.
dot_numbers = [] # Keep track of dot numbers


# Function to process the sentence segmentation heuristic.
with open(eng_file, 'r') as f, open(sum_file, 'r') as g:

	i=0
	temp_file1 = []
	temp_file2 = []

	for line in f:
		line = line.strip()
		split_line = line.split()
		if '.' not in split_line:
			for item in split_line:
				temp_file1.append(item)
			i+=1
		else:
			for item in split_line:
				temp_file1.append(item)
			dot_numbers.append(i)
			i+=1
			sentence = ' '.join(temp_file1)
			file1.append(sentence.strip())
			temp_file1 = []
	

	j=0
	for line in g:
		line = line.strip()
		split_line = line.split()
		if j in dot_numbers:
			j+=1
			for item in split_line:
				temp_file2.append(item)
			sentence = ' '.join(temp_file2)
			file2.append(sentence.strip())
			temp_file2 = []
		else:
			for item in split_line:
				temp_file2.append(item)
			j+=1



# Write to the new files
with open(OUTPUT_ENG_FILE, 'w+') as o, open(OUTPUT_SUM_FILE, 'w+') as p:
	for item in file1:
		o.write(item)
		o.write('\n')
	for item in file2:
		p.write(item)
		p.write('\n')








	