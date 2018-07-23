############################################################
# Script for compressing SRL Sumerian tags

# Pre-requisites: - 

# Usage : python3 fixsrl2conll.py SUM_PROJECTED_FILE
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
			

			print ("LINE NO: ", m_line_no)
			flag_predicate = 0
			

			m_line_no+=1 # Increment line no. only when we encounter a blank token
			

			for item in intermediate_lines:
				#Check if predicate exists in any one of the item of the intermediate lines
				if item[2] == 'Y':
					flag_predicate += 1 #increments to find no. of predicates.

			#create an index to column no. dict
			index_to_column ={}
			c = 4
			#initialise all index_to_column dict
			for i in range(1, flag_predicate+1):
				index_to_column[i] = c
				c+=1


			for item in intermediate_lines

			# If no predicate, skip the sentence altogether since it does not have 13 and 14 indexes
			if flag_predicate == 0:
				for i, item in enumerate(intermediate_lines):
					if (i==0):
						continue
					string = '\t'.join(x for i, x in enumerate(item))
					projected_list.append(string.strip())

				projected_list.append('\n')
				intermediate_lines = []
				intermediate_lines.append(['0','-','0','-','-','-'])
				copy_intermediate_lines = []
				continue


			
			
			

			projected_list.append('\n')
			intermediate_lines = []

			continue

		line = line.split('\t')
		intermediate_lines.append(line)


# Store the fixed mate tools extended output
with open('../../outputs/projected/new_srl_compressed_projection.out', 'w+') as f:
	for item in projected_list:
		#print (item)
		if item == '\n':
			f.write(item)
		else:
			f.write(item+'\n')











