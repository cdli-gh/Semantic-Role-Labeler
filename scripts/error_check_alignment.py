import os,sys

total = 0
err = 0
with open(sys.argv[1], 'r') as f:
	for line in f:
		total+=1
		line  = line.lower().split()
		if 'error' in line:
			err+=1

print ("Error-prone : ")
print (float(err)/total * 100 )
