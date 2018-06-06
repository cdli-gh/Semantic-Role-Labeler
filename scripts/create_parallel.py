import sys, os
import numbers, codecs

SUM_DIR = sys.argv[1]
ENG_DIR = sys.argv[2]

eng_list = os.listdir(ENG_DIR)
sum_list = os.listdir(SUM_DIR)

bad_files = [] #create a file where proper alignment is not maintained

for eng_file in eng_list:

	# Find equivalent Sumerian file for the English translations
	sum_file = ''.join(eng_file)
	sum_file = 'c' + sum_file[1:]

	line_ranges = []
	contents_eng = [] # Store eng lines for a particular file
	contents_sum = []

	print (sum_file)
	print (eng_file)

	with codecs.open(ENG_DIR+eng_file, 'r', encoding='utf-8') as e, codecs.open(SUM_DIR+sum_file, 'r', encoding='utf-8') as s:
		next(e)  # Skip the first line
		next(s)
		for line in e:
			line = line.split('\t')


			#Boundary conditions
			if len(line) < 4 or '-' not in line[3]:
				bad_files.append(eng_file)
				continue
			try:
				b = int(line[3].split('-')[0])
				c = int(line[3].split('-')[1])
			except:
				continue
			
			if len(line[3].split('-'))==2:
				line_ranges.append(int(line[3].split('-')[0]))
				line_ranges.append(int(line[3].split('-')[1]))
			else:
				line_ranges.append(int(line[3]))


			if (line[4]==''):
				print ("EMPTY : ", eng_file)
			contents_eng.append(line[4])


		
		i=0
		temp_string = ''
		for line in s:
			line = line.split(',')

			#Boundary condition if line_ranges ends
			if (i+1) >= len(line_ranges):
				temp_string = temp_string + line[4]
				contents_sum.append(temp_string)
				temp_string = ''
				continue

			# Error handling
			try:
				a = int(line[3])
			except:
				bad_files.append(eng_file)
				continue
		
			if int(line[3]) in list(range(line_ranges[i]+1, line_ranges[i+1]+1)):
				temp_string = temp_string + line[4] + ' '
				continue
			temp_string = temp_string.strip()
			contents_sum.append(temp_string)
			temp_string = ''
			i+=1

		#print (contents_eng)
		#print (contents_sum)
		if eng_file not in bad_files:
			with codecs.open('../inputs/parallel-etcsl-eng/'+eng_file, 'w+') as pe, codecs.open('../inputs/parallel-etcsl-sum/'+sum_file, 'w+') as ps:
				for item in contents_eng:
					pe.write(item)
					#pe.write('\n')
				for item in contents_sum:
					ps.write(item)
					ps.write('\n')








