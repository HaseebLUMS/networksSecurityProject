'''
Name: local_dependency_finder.py
Output: Device Annotation
What does it do:
	From a set of possible annotations, finds actual 
	device annotation by finding local dependencies 
	(defind in ARE paper) from web page text
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
def linefyText(text): 
	text = text.replace("\n", ". ")
	return text.split(". ")

'''
Counts the lines in text
which contains the term "a"
or term "b" where as "a" and
"b" are variables
'''
def count_related_lines(a, b, text):

	count = 0
	tmp = ""
	for t in text:
		if (a in t.lower()) and (b in t.lower()):
			# print(t)
			for word in t.lower().split(" "):
				if word == a:
					tmp += 'v'
				if word == b:
					tmp += 'd'
			
			if('vd' in tmp):
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

	anns = [] #annotations	
	ans_ven = ''
	ans_dev = ''
	# print(vendors, device_types)
	for v in vendors:
		if len(v) < 3: continue
		for d in device_types:
			count = count_related_lines(v, d, text)
			if count: #v and d are already sorted so the first one with a depen
						#dency is answer
				ans_ven = v
				ans_dev = d
				anns.append({'vendor': ans_ven, 'device_type': ans_dev})

			# if  count > max_lines:
			# 	max_lines = count
			# 	ans_ven = v
			# 	ans_dev = d
	
	print(anns)
	return anns[0]


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
			if ((a.lower() in line.lower()) and (b.lower() in line.lower()) and ((t.lower()) in line.lower())):
				count += 1
			# elif ((a.lower() in line.lower()) and (b.lower() in line.lower()) and ((t.lower()+'. ') in line.lower())):
			# 	count += 1
		if count > max_lines:
			max_lines = count
			ans_prod = t

	return ans_prod


'''
Finds Local Dependecies between possible
annotations and prints results
'''
def main():
	print('Finding Local Dependecies.')
	global file
	global vendors
	global device_types
	global products

	text = linefyText(file)
	predicted_label = {}
	try: predicted_label = find_dependency(text, vendors, device_types)
	except: pass
	
	
	ans = ""
	try:
		print('Brand: ', predicted_label['vendor'].upper())
		ans = predicted_label['vendor'].upper() + " | "
	except:
		pass

	
	try:
		print('Device: ', predicted_label['device_type'].upper())
		ans = ans + predicted_label['device_type'].upper()
	except:
		pass

	try:
		predicted_product = find_product(text, predicted_label['vendor'], predicted_label['device_type'], products)
	except:
		pass

	try:
		if predicted_product and (predicted_product is not ''):
			print('Product Number: ', predicted_product)
			ans =  ans + " | " + predicted_product
	except:
		pass	
	
	with open('annotation.txt', 'w') as f:
		f.write(ans)

main()
