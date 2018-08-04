############################################################
# Script for conversion of finer SRL output to coarser tagset.
# Basically, what this does is replacement of A0-A4 to Level-1(L1)
# and other tagsets to Level-2(i.e. L2)
#
# Pre-requisites: - 

# Usage : python3 fine2coarse.py GOLD_SUMERIAN_SRL_FILE OUTPUT_FILE
############################################################


import sys, os, copy
GOLD_SUMERIAN_SRL_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
# define the level-1 and level-2 labels

l1 = ['A0', 'A1', 'A2', 'A3', 'A4', 'O']
l2 = ['AM-DIS', 'AM-ADV', 'AM-DIR', 'R-A0', 'AM-NEG', 'R-AM-TMP', 'R-AM-LOC','AM-CAU', 'R-A1','AM-PNC','AM-MOD','AM-MNR','AM-LOC','AM-EXT','AM-TMP']

final_file = []
with open(GOLD_SUMERIAN_SRL_FILE, 'r') as f:

	for line in f:
		line = line.strip().split('\t')


		if line[0] == '':  # i.e. if it marks the end of a sentence, skip that empty line
			final_file.append('\n')
			continue

		# Main algorithm
		copy_line = copy.deepcopy(line)
		for i, item in enumerate(line): # all labels will be from position 9 and onwards...
			#Check for level 1
			for label in l1:
				if label in item:
					#print (label)
					#print ("OLD LABEL", line[i])
					#print (line[i].replace(str(label), "L1"))
					copy_line[i] = line[i].replace(str(label), "L1") #List slicing creates another object so does not modify original list! :(
					#print ("NEW LABEL", copy_line[i])

			for label in l2:
				if label in item:
					copy_line[i] = line[i].replace(label, 'L2')

		copy_line = '\t'.join(copy_line)
		copy_line = copy_line.strip()
		final_file.append(copy_line)
		final_file.append('\n')

with open(OUTPUT_FILE,'w+') as g:
	for item in final_file:
		g.write(item)

print ("Success!")






