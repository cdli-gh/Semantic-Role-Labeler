############################################################
# Script for compressing SRL Sumerian tags

# Pre-requisites: - 

# Usage : python3 compres_projection.py SUM_PROJECTED_FILE
############################################################

import sys, os
import collections # for OrderedDict

projected_list = []

with open(SUM_PROJECTED_FILE, 'r') as f:
	m_line_no = 1

	intermediate_lines = []
	projected_list = []

	for line in f:


		line = line.strip() # to remove newline characters at the end of the line
		
		# Once an end of an actual line occurs :-
		if line == '':
			# Make a dictionary for each intermediate line to keep track of duplicates
			track_dict = {}


			print ("LINE NO: ", m_line_no)
			flag_predicate = 0
			

			m_line_no+=1 # Increment line no. only when we encounter a blank token

			for i, item in enumerate(intermediate_lines):
				if i==0:
					track_dict[i] = []
					track_dict[i].append(i)

				if intermediate_lines[i][1] == intermediate_lines[i-1][1]:
					track_dict[i-1].append(i)
				else:
					track_dict[i] = []
					track_dict[i].append(i)


			# Make an ordered dict.
			od_track_dict = collections.OrderedDict(sorted(track_dict.items()))

			token_no = 1
			# Algorithm for merge here
			for key, value in od_track_dict.items():
				if len(value)==1:
					projected_list.append(intermediate_lines[key])
					

				token_no+=1











				#Check if predicate exists in any one of the item of the intermediate lines
				if item[12] == 'Y':
					flag_predicate = 1
			'''
			# If no predicate, skip the sentence altogether since it does not have 13 and 14 indexes
			if flag_predicate == 0:
				for i, item in enumerate(intermediate_lines):
					string = '\t'.join(x for i, x in enumerate(item))
					projected_list.append(string.strip())

				projected_list.append('\n')
				intermediate_lines = []
				copy_intermediate_lines = []
				continue
			'''

			copy_intermediate_lines = copy.deepcopy(intermediate_lines)
			
			for i,item in enumerate(copy_intermediate_lines):
				string = '\t'.join(x for i, x in enumerate(item))
				projected_list.append(string.strip())

			projected_list.append('\n')
			intermediate_lines = []
			copy_intermediate_lines = []

			continue

		line = line.split('\t')
		intermediate_lines.append(line)


# Store the fixed mate tools extended output
with open('../../outputs/mate-parsing/un-normalised/extended_translated_eng_train_mate_unnorm.dat', 'w+') as f:
	for item in projected_list:
		if item == '\n':
			f.write(item)
		else:
			f.write(item+'\n')











