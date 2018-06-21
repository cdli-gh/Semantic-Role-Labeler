############################################################
# Script for running mate-tools on the data

# Pre-requisites: 1. Java installed on your machine.
#				  2. Install the mate-tools python wrapper from 'https://github.com/bjut-hz/py-mate-tools'

# Usage : python mateparsing.py [input_file] [output_path]
# Note : The output path must be a directory to which results.out is written. DON'T SPECIFY A FILE PATH HERE!!!
############################################################

import sys, os, codecs
from PyMateTools import matetools

INPUT_FILE = sys.argv[1]

OUTPUT_PATH = sys.argv[2]
OUTPUT_PATH = os.path.abspath(OUTPUT_PATH) # get the absolute path of the output file you want to write to

# Make the mate_tools object for calling the Python wrapper
mate_tools = matetools.MateTools()

# Read the file
print ("Reading the file ...")
data = []
with codecs.open(INPUT_FILE, 'r', encoding='utf-8') as f: #resolved utf-8 encoding issue with mate-tools...
	for line in f:
		data.append(line.strip())


# Do the parsing using mate-tools
print ("Parsing ...")
mate_tools.SRL( data, verbose = True, result_file_path = OUTPUT_PATH)

print ("Done.")