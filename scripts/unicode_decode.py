############################################################
# Script for normalising the english character set in the source Eng data
# Usage : python [input_file] [output_file]
#
############################################################
from unidecode import unidecode
import sys
import codecs

INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]


# Store the lines here
lines = []

# Read the input file and process it with the unidecode module to transfer the unicode to
#  the nearest ASCII character
with codecs.open(INPUT_FILE, 'r', encoding='utf-8') as f:
	for line in f:
		#print (type(line), line)
		line = unidecode(line)
		#print (type(line), line)
		lines.append(line)

with open(OUTPUT_FILE, 'w+') as f:
	for item in lines:
		f.write(item)


