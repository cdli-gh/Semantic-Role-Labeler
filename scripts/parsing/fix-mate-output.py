############################################################
# Script for fixing arguments of prepositional phrases in output of mate-tools

# Pre-requisites: - 

# Usage : python3 fix-mate-output.py ENG_MATE_PARSED_FILE
############################################################

import sys, os
import copy

ENG_MATE_PARSED_FILE = sys.argv[1]
projected_list = [] #Store fixed output here


def dfs(dictionary, temp_list, start, depth):
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
		dfs(children, temp_list, item, depth)



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
			children['0'] = []

			for item in intermediate_lines:
				parent[item[0]] = item[9]
				children[item[0]] = []

				#Check if predicate exists in any one of the item of the intermediate lines
				if item[12] == 'Y':
					flag_predicate = 1

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



			for key, val in parent.items():
				#print (key, val)
				#print (type(key), type(val))
				if key != val:
					children[val].append(key)

				#print (children[val])

			print (children)
			for key, val in children.items():
				temp_list = []
				depth =0
				#temp_list.append(key)
				dfs(children, temp_list, key, depth)
				print ("NEW LIST : ",temp_list)
				children[key] = temp_list

			#print (children)
			copy_intermediate_lines = copy.deepcopy(intermediate_lines)
			print (children)
			#print (copy_intermediate_lines)
			for key, arr in children.items():
				if key == '0':
					continue

				if (intermediate_lines[int(key)][14] != '_'):
					#print (intermediate_lines[int(key)][14])
					#print (arr)
					#copy_intermediate_lines[int(key)][14] = intermediate_lines[int(key)][14]
					#print (copy_intermediate_lines)
					for child in arr:
						copy_intermediate_lines[int(child)][14] = intermediate_lines[int(key)][14]
						#print (copy_intermediate_lines[int(child)][14])
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
with open('../../outputs/mate-parsing/un-normalised/extended_translated_eng_train_mate_unnorm.dat', 'w+') as f:
	for item in projected_list:
		f.write(item+'\n')










