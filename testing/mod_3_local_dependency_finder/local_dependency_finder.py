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

selected_text = []

''' Separate the lines of 
the text and makes a list
'''
def linefy_text(text): 
	text = text.replace(".\n", ". ")
	text = text.replace("\n", ". ")
	# print(text.split(". "))
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
				selected_text.append(t)
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
			# print("=> ", count)
			if count: #v and d are already sorted so the first one with a depen
						#dency is answer
				ans_ven = v
				ans_dev = d
				anns.append({'vendor': ans_ven, 'device_type': ans_dev})

			# if  count > max_lines:
			# 	max_lines = count
			# 	ans_ven = v
			# 	ans_dev = d
	
	return anns

def all_indices(token, text):
	ans = [-1]
	index = 0
	for ind, ele in enumerate(text.split(" ")):
		index += len(ele)
		if token.lower() == ele.lower():
			ans.append(index)
		index += 1
	return ans

'''
from a given list of possible product names,
it finds whether any line contains terms a and b
alongwith a product name where as a and b are 
variables (device annotations, in practice).
'''
def find_product(text, a, b, tags):
	ans_prod = set({})

	for t in tags:
		for line in text:
			if t.lower() in line.lower():
				ind_a = line.lower().find(a.lower())
				ind_b = line.lower().find(b.lower())
				if ind_a is -1: ind_a = len(line)
				if ind_b is -1: ind_b = len(line)
				ind_t = all_indices(t, line)[-1] #largest product index
				any_lower_ab = False
				tt = ind_t
				if ind_a < tt or ind_b < tt:
					any_lower_ab = True
				# print(tt, a, b, ind_a, ind_b)
				if any_lower_ab == True:
					ans_prod.add(t.upper())
					# print(ans_prod)
					break

	return list(ans_prod)


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

	text = linefy_text(file)
	predicted_labels = []
	try: predicted_labels = find_dependency(text, vendors, device_types)
	except: pass
	
	with open("annotation.txt", "w") as f: f.write("") #clearing the file


	for predicted_label in predicted_labels:
		ans = ""
		try:
			ans = predicted_label['vendor'].upper() + " | "
		except:
			pass
		
		try:
			ans = ans + predicted_label['device_type'].upper()
		except:
			pass

		text = selected_text #narrows down the text to the lines containing vendor and devices
		# try:
		predicted_products = find_product(text, predicted_label['vendor'], predicted_label['device_type'], products)
		# except Exception as e:
			# print(e)
			# pass

		prev_ans = ans
		for predicted_product in predicted_products:
			ans = prev_ans
			try:
				if predicted_product and (predicted_product is not ''):
					ans =  ans + " | " + predicted_product
			except:
				pass	
			
			with open('annotation.txt', 'a+') as f:
				print(ans)
				f.write(ans+"\n")

main()
