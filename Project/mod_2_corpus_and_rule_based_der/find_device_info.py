import sys
import os


file = sys.argv[1]


'''
Returns the predicted labels

It uses the file ind.json made by JS code in file index.js
and other data file (vendors or device_types) given as command line
argument.
It searches the ind.json file for every term present in data files
(vendors or device_types) by internally running index.js code (by searchx mode).
Then it just reports the most frequent label.
'''
def find_DI():
	words = []

	with open(file, 'r') as f:  
		line = f.readline()
		while line:
			words.append(line.rstrip())
			line = f.readline()


	frequent = ''
	fr       = 0
	frResult = []
	ambigious = False

	for w in words:
		comm = 'node index.js searchx ind.json \'["' + w + '"]\''
		res = os.popen(comm).read()
		res = res.split('\n')
		result = []
		for r in res:
			if r != '': result.append(r)
		if len(result) > fr:
			if len(result) - fr < 5: ambigious = True
			else: ambigious = False 
			fr = len(result)
			frequent = w
			frResult = result

	print(frequent)
	if ambigious:
		print('ambigious? =>', ambigious)
	else:
		print('Not ambigious.')

find_DI()