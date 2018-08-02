############################################################
# Script for compressing SRL Sumerian tags

# Pre-requisites: - 

# Usage : python3 compress_projection.py SUM_PROJECTED_FILE
############################################################

import sys, os
import copy # for deepcopy
import collections # for OrderedDict

projected_list = []

SUM_PROJECTED_FILE = sys.argv[1]
with open(SUM_PROJECTED_FILE, 'r') as f:
	m_line_no = 1

	intermediate_lines = [] #
	projected_list = [] #Final output file stored line-by-line.

	for line in f:


		line = line.strip() # to remove newline characters at the end of the line
		
		# Once an end of an actual line occurs :-
		if line == '':
			# Make a dictionary for each intermediate line to keep track of duplicates
			track_dict = {}

			print ("LINE NO: ", m_line_no)
			flag_predicate = 0
			

			m_line_no+=1 # Increment line no. only when we encounter a blank token
			x = 0 # Keep track of already numbers in dict.
			for i, item in enumerate(intermediate_lines):
				if i==0:
					track_dict[i] = []
					track_dict[i].append(i)
					x = i

				if intermediate_lines[i][1] != intermediate_lines[i-1][1]:
					x = i
					track_dict[i] = []
					track_dict[i].append(i)
				elif intermediate_lines[i][1] == intermediate_lines[i-1][1]:
					track_dict[x].append(i)

			# Make an ordered dict.
			od_track_dict = collections.OrderedDict(sorted(track_dict.items()))

			
			pred_pos = {} #Dict for storing the position of the predicate, re-


			token_no = 1
			
			# Algorithm for finding predicates and other related stuff
			for key, value in od_track_dict.items():
				for item in value:
					if intermediate_lines[item][2] == 'Y':
						pred_pos[key] = item

			# Algorithm for compression
			for key, value in od_track_dict.items():

				if key not in pred_pos: # Normal tag
					intermediate_lines[key][0] = str(token_no)
					projected_list.append('\t'.join(x for i, x in enumerate(intermediate_lines[key])))
				else:
					intermediate_lines[pred_pos[key]][0] = str(token_no)
					projected_list.append('\t'.join(x for i, x in enumerate(intermediate_lines[pred_pos[key]])))
				token_no+=1


			projected_list.append('\n')
			intermediate_lines = []

			continue

		line = line.split('\t')
		intermediate_lines.append(line)


# Store the fixed mate tools extended output
with open('../../outputs/projected/test_srl_compressed_projection.out', 'w+') as f:
	for item in projected_list:
		#print (item)
		if item == '\n':
			f.write(item)
		else:
			f.write(item+'\n')











