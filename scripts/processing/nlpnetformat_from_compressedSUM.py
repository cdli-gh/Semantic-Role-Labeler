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
	intermediate_lines.append(['0','-','0','-','-','-','-'])

	projected_list = [] #Final output file stored line-by-line.
	magic = 1
	for line in f:



		line = line.strip() # to remove newline characters at the end of the line
		
		# Once an end of an actual line occurs :-
		if line == '':
			

			#print ("LINE NO: ", m_line_no)
			#print (" MAGIC NO: ", magic)
			#for item in intermediate_lines:
			#	print (item[1])
			flag_predicate = 0
			

			m_line_no+=1 # Increment line no. only when we encounter a blank token
			
			#print (intermediate_lines)
			for item in intermediate_lines:
				#Check if predicate exists in any one of the item of the intermediate lines
				if item[2] == 'Y':
					flag_predicate += 1 #increments to find no. of predicates.

			#create an index to column no. dict
			index_to_column ={}
			c = 4

			#initialise chunks
			chunks={}

			#initialise all index_to_column dict
			for i in range(1, flag_predicate+1):
				chunks[c] ={}
				index_to_column[i] = c
				for i, item in enumerate(intermediate_lines):
					if (i==0):
						continue

					#print (chunks)
					#print ("c : item", c, item)
					#print ("items : ", item[1], c, item[c])
					if (item[c] not in chunks[c]) and item[c] != '_' and item[c] != '-':
						chunks[c][item[c]] = []
					if (item[c] == '_' or item[c] == '-'):
						continue
					chunks[c][item[c]].append(item[0])
				c+=1



			# If no predicate, skip the sentence altogether since it does not have 13 and 14 indexes
			if flag_predicate == 0:
				for i, item in enumerate(intermediate_lines):
					if (i==0):
						continue
					string = '\t'.join(x for i, x in enumerate(item))
					projected_list.append(string.strip())

				projected_list.append('\n')
				intermediate_lines = []
				intermediate_lines.append(['0','-','0','-','-','-','-'])

				copy_intermediate_lines = []
				continue

			copy_intermediate_lines = copy.deepcopy(intermediate_lines)


			#iterate through it
			for index, val in chunks.items():
				start = 0
				end = 0
				
				for key, arr in chunks[index].items():

					temp_arr = sorted(arr)
					print ("KEY , ARR : ", key, temp_arr)
					for i, item in enumerate(temp_arr):
						if (i==0) and len(temp_arr) == 1:
							#print ("item :", item)
							copy_intermediate_lines[int(item)][(int(index))] = '(' + key + '*)'
							continue
						elif (i==0) and len(temp_arr) > 1:
							copy_intermediate_lines[int(item)][(int(index))] = '(' + key + '*'
							print (copy_intermediate_lines[int(item)][(int(index))])
							continue
						if (i == (len(temp_arr)-1)):
							copy_intermediate_lines[int(item)][(int(index))] = '*)'
						else:
							copy_intermediate_lines[int(item)][int(index)] = '*'

					for i, item in enumerate(copy_intermediate_lines):
						if (i==0):
							continue
						#if '*' not in item[int(index)]:
					#		copy_intermediate_lines[i][int(index)] = '*'



			for i,item in enumerate(copy_intermediate_lines):
				if (i==0):
					continue
				string = '\t'.join(x for i, x in enumerate(item))
				projected_list.append(string.strip())

			projected_list.append('\n')
			intermediate_lines = []
			intermediate_lines.append(['0','-','0','-','-','-','-'])

			copy_intermediate_lines = []

			continue


		line = line.split('\t')
		intermediate_lines.append(line)
		magic+=1


# Store the fixed mate tools extended output
with open('../../outputs/projected/intermediate_srl_compressed_projection.out', 'w+') as f:
	for item in projected_list:
		#print (item)
		if item == '\n':
			f.write(item)
		else:
			f.write(item+'\n')











