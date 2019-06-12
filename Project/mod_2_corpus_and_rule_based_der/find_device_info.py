'''
Name: find_device_info.py
Argument: 	Database file (e.g vendors or device_types)
Output: 	Predicted Labels
How to run: python3 find_device_info.py db_name
			e.g python3 find_device_info.py vendors
What does it do:
			--reads the databse files and stores as "words"
			--runs the index.js for each word in words (uses ind.json)
			--records the output of index.js
			--computes the most frequent term of ind.json appearing in 
			  "words"
			--reports that term as predicted label
'''


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
	global file
	words = [] #Stores the terms of database provided as argument
	with open(file, 'r') as f:  
		line = f.readline()
		while line:
			words.append(line.rstrip())
			line = f.readline()
	frequent = '' #Will store the most frequent term
	fr       = 0  #helping var for frequent
	# frResult = [] #
	ambigious = False
	for w in words:
		comm = 'node ./mod_2_corpus_and_rule_based_der/index.js searchx ./mod_2_corpus_and_rule_based_der/Database/ind.json \'["' + w + '"]\''
		# print("Error May Be Here", comm)
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
			# frResult = result
	print(" => ", frequent.upper())
	# if ambigious:
	# 	print('ambigious? =>', ambigious)
	# else:
	# 	print('Not ambigious.')



'''Runs the find_DI() '''
def main():
	find_DI()

main()