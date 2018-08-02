############################################################
# Script for fixing arguments of prepositional phrases in output of mate-tools

# Pre-requisites: - 

# Usage : python3 fix-mate-output.py ENG_MATE_PARSED_FILE
############################################################

import sys, os
import copy

ENG_MATE_PARSED_FILE = sys.argv[1]
projected_list = [] #Store fixed output here


def dfs(dictionary, temp_list, start, depth, index):
	print ("DICTIONARY: ", dictionary)
	print ("START : ", start)
	print ("TEMP_LIST :", temp_list)
	if start in temp_list:
		return
	if len(dictionary[start]) == 0:
		temp_list.append(start)
		return
	if depth !=0:
		temp_list.append(start)
	depth+=1
	for item in dictionary[start]:
		print ("ITEM :", item)
		dfs(children[index], temp_list, item, depth, index)



with open(ENG_MATE_PARSED_FILE, 'r') as f:
	m_line_no = 1

	intermediate_lines = []
	intermediate_lines.append(['0','-','-','-','-','-','-','-','-','0','-','-','-','-'])
	projected_list = []
	for line in f:

		line = line.strip() # to remove newline characters at the end of the line
		
		# Once an end of an actual line occurs :-
		if line == '':
			print ("LINE NO: ", m_line_no)
			flag_predicate = 0
			# Create the parent and children dicts.
			# parent is one-to-one.
			# children is one-to-a-list.
			parent = {}
			children = {}

			m_line_no+=1 # Increment line no. only when we encounter a blank token

			#Find all parents of lines


			for item in intermediate_lines:
				parent[item[0]] = item[9]
				#children[item[0]] = [] modified - do not initialise here.

				#Check if predicate exists in any one of the item of the intermediate lines
				if item[12] == 'Y':
					flag_predicate += 1 #increments to find no. of predicates.

			
			#create an index to column no. dict
			index_to_column ={}
			c = 14
			#initialise all children dicts:
			for i in range(1, flag_predicate+1):
				children[i] = {}
				children[i]['0'] = []
				index_to_column[i] = c
				c+=1
				for item in intermediate_lines:
					children[i][item[0]] = [] # initialise here.


			# If no predicate, skip the sentence altogether since it does not have 13 and 14 indexes
			if flag_predicate == 0:
				for i, item in enumerate(intermediate_lines):
					if (i==0):
						continue
					string = '\t'.join(x for i, x in enumerate(item))
					projected_list.append(string.strip())

				projected_list.append('\n')
				intermediate_lines = []
				intermediate_lines.append(['0','-','-','-','-','-','-','-','-','0','-','-','-','-'])
				copy_intermediate_lines = []
				continue


			#print (children)
			copy_intermediate_lines = copy.deepcopy(intermediate_lines)
			#print (children)
			#print (copy_intermediate_lines)


			for index, value in children.items():

				for key, val in parent.items():
					#print (key, val)
					#print (type(key), type(val))
					if key != val:
						children[index][val].append(key)

					#print (children[val])

				#print (children)
				for key, val in children[index].items():
					temp_list = []
					depth =0
					#temp_list.append(key)
					dfs(children[index], temp_list, key, depth, index)
					print ("NEW LIST : ",temp_list)
					children[index][key] = temp_list



				for key, arr in children[index].items():
					if key == '0':
						continue

					if (intermediate_lines[int(key)][index_to_column[index]] != '_'):
						#print (intermediate_lines[int(key)][14])
						#print (arr)
						#copy_intermediate_lines[int(key)][14] = intermediate_lines[int(key)][14]
						#print (copy_intermediate_lines)
						arr_len = len(arr)
						for x, child in enumerate(sorted(arr)):
							copy_intermediate_lines[int(child)][index_to_column[index]] = intermediate_lines[int(key)][index_to_column[index]]
							'''
							if x == 0:
								copy_intermediate_lines[int(child)][index_to_column[index]] = "(" + intermediate_lines[int(key)][index_to_column[index]] + "*"
							
							copy_intermediate_lines[int(child)][index_to_column[index]] = "*"

							if (x == arr_len-1):
								copy_intermediate_lines[int(child)][index_to_column[index]] = ")"
							#print (copy_intermediate_lines[int(child)][14])
							'''
				
				'''
				#For the remaining which did not have * yet.
				for i, item in enumerate(copy_intermediate_lines):
					if (i==0):
						continue
					if (copy_intermediate_lines[i][index_to_column[index]] == '_'):
						copy_intermediate_lines[i][index_to_column[index]] = '*'
				'''

			print (copy_intermediate_lines)

			for i,item in enumerate(copy_intermediate_lines):
				if (i==0):
					continue
				string = '\t'.join(x for i, x in enumerate(item))
				projected_list.append(string.strip())
			projected_list.append('\n')
			intermediate_lines = []
			intermediate_lines.append(['0','-','-','-','-','-','-','-','-','0','-','-','-','-'])
			copy_intermediate_lines = []

			continue

		line = line.split('\t')
		intermediate_lines.append(line)


# Store the fixed mate tools extended output
with open('../../outputs/mate-parsing/un-normalised/test_srl_extended_translated_eng_train_mate_unnorm.dat', 'w+') as f:
	for item in projected_list:
		if item == '\n':
			f.write(item)
		else:
			f.write(item+'\n')










