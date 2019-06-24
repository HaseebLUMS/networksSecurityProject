'''
Name: local_dependency_finder.py
Output: Device Annotation
What does it do:
	From a set of possible annotations, finds actual 
	device annotation by finding local dependencies 
	(defind in ARE paper) from web page test
'''


import os
import sys
import re
import json


with open(sys.argv[1], 'r') as f: predictions = json.loads(f.read())
with open(sys.argv[2], 'r') as f: file = f.read()

vendors = predictions['vendors']
device_types = predictions['device_types']
products = predictions['products']


''' Separate the lines of 
the text and makes a list
'''
def linefyText(text): return re.split('[.]', text)


'''
Counts the lines in text
which contains the term "a"
or term "b" where as "a" and
"b" are variables
'''
def count_related_lines(a, b, text):

	count = 0
	for t in text:
		if (a in t.lower()) and (b in t.lower()):
			# print(t)
			count += 1
	# if a is 'mikrotik':
	# 	print(count)
	return count



'''
Finds local dependencies
in text.
Two kinds of local dependency usually occur: 
(1) the vendor, device type and product appears 
in a line
(2) There might not be product in the line.
If the relationship is established and matches any of these two 
dependency rules, DER will select the tuple (device type, vendor, product)
'''
def find_dependency(text, vendors, device_types):

	max_lines = 0
	ans_ven = ''
	ans_dev = ''
	# print(vendors, device_types)
	for v in vendors:
		if len(v) < 3: continue
		for d in device_types:
			count = count_related_lines(v, d, text)
			# print('For ', v , ' and ', d, ' ', count)
			if count: #v and d are already sorted so the first one with a depen
						#dency is answer
				ans_ven = v
				ans_dev = d
				return {'vendor': ans_ven, 'device_type': ans_dev}

			# if  count > max_lines:
			# 	max_lines = count
			# 	ans_ven = v
			# 	ans_dev = d
	



'''
from a given list of possible product names,
it finds whether any line contains terms a and b
alongwith a product name where as a and b are 
variables (device annotations, in practice).
'''
def find_product(text, a, b, tags):
	max_lines = 0
	ans_prod = ''

	for t in tags:
		count  = 0
		for line in text:
			if ((a in line) and (b in line) and (t in line)):
				count += 1
		if count > max_lines:
			max_lines = count
			ans_prod = t

	return ans_prod


'''
Finds Local Dependecies between possible
annotations and prints results
'''
def main():
	global file
	global vendors
	global device_types
	global products

	text = linefyText(file)
	predicted_label = find_dependency(text, vendors, device_types)
	print('Brand: ', predicted_label['vendor'].upper())
	print('Device: ', predicted_label['device_type'].upper())
	ans = predicted_label['vendor'].upper() + ' | ' + predicted_label['device_type'].upper()


	predicted_product = find_product(text, predicted_label['vendor'], predicted_label['device_type'], products)
	if predicted_product is not '' and predicted_label['vendor'] is not '':
		print('Product Number: ', predicted_product)
		ans =  ans + " | " + predicted_product
	
	
	with open('annotation.txt', 'w') as f:
		f.write(ans)

main()
