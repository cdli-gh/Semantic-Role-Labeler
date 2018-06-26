############################################################
# Script for projecting SRL tags onto Sumerian

# Pre-requisites: - 

# Usage : python3 projection.py WORD_ALIGNED_FILE MATE_PARSED_FILE
############################################################

import sys, os

WORD_ALIGNED_FILE = sys.argv[1]
MATE_PARSED_FILE = sys.argv[2]

# Create a dictionary that holds the English to Sumerian alignments.
# This will have a nested structure, so that we have a dictionary to hold
# alignments for each line in the word-aligned corpus.

alignment = {}
#Assume length of file is not more than 19k sentences for now. Must be changed as corpus size increases.
range_list = [str(x) for x in range(0, 20000)]

for i in range(0, 20000):
	alignment[str(i)] = {}


with open(WORD_ALIGNED_FILE, 'r') as f:
	a_line_no = 1
	for line in f:
		line = line.split()

		# create a placeh

		for item in line:
			if '|' in item:
				item = item.split('|')

				alignment[str(a_line_no)][item[1]] = item[0]

		a_line_no+=1

projected_list = [] #this will store the projection file here, in conll format 

with open(MATE_PARSED_FILE, 'r') as f:
	m_line_no = 1
	#check = 1
	for line in f:
		#if (check > 1):
		#	break
		print (line)
		line = line.strip() # to remove newline characters at the end of the line
		
		# Once an end of an actual line occurs :-
		if line == '':
			#print (projected_list)
			projected_list.append('\n')
			m_line_no+=1 # Increment line no. only when we encounter a blank token
			continue
		line = line.split('\t')

		# Strip the LEMMA and PLEMMA columns for Sumerian projection
		line[2] = '-'
		line[3] = '-'

		# Replace the FORM column with existing Sumerian word from the alignment dict.
		try:
			line[1] = alignment[str(m_line_no)][line[1]]
		except:
			print ("Alignment not found | ", line[1], " | Line no. " ,m_line_no)
			continue
		# Check if the token is a predicate -  if yes, replace the column pertaining to that with the sumerian word.
		if line[12] == 'Y':
			label = line[13].split('.')[1] # Check if .01 or .02
			try:
				line[13] = alignment[str(m_line_no)][line[1]] # Find word alignment
			except:
				line[13] = line[13].split('.')[0] # If no success, replace with the Eng word
				pass
			if label == '01':
				line[13] = line[13] + '.01'
			elif label == '02':
				line[13] = line[13] + '.02'

			else:
				print ('label .01 or .02 does not exist for the predicate.', m_line_no)


		#Join the line_no for error handling
		#line.append(str(m_line_no))
		# Join the list into a string and append it to the final projected list
		string = '\t'.join(x for i, x in enumerate(line) if (i==0 or i==1 or i>=12) )
		string = string.strip()
		projected_list.append(string)

		#check+=1


# Store the projected output
with open('../../outputs/projected/new_cleaned_projected.out', 'w+') as f:
	for item in projected_list:
		f.write(item+'\n')



print (alignment['1'])











