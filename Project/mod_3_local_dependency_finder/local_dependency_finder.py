import os
import sys
import re
import json


with open(sys.argv[1], 'r') as f: predictions = json.loads(f.read())
with open(sys.argv[2], 'r') as f: file = f.read()

vendors = predictions['vendors']
device_types = predictions['device_types']
products = predictions['products']


def linefyText(text): return re.split('[.]',text)


def count_related_lines(a, b, text):
	count = 0
	for t in text:
		if (a in t) and (b in t):
			count += 1
	return count


def find_dependency(text, vendors, device_types):

	max_lines = 0
	ans_ven = ''
	ans_dev = ''
	for v in vendors:
		for d in device_types:
			count = count_related_lines(v, d, text)
			if  count > max_lines:
				max_lines = count
				ans_ven = v
				ans_dev = d
	
	return {'vendor': ans_ven, 'device_type': ans_dev}


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


def main():
	global file
	global vendors
	global device_types
	global products

	text = linefyText(file)
	predicted_label = find_dependency(text, vendors, device_types)
	print('Brand: ', predicted_label['vendor'].upper())
	print('Device: ', predicted_label['device_type'].upper())

	predicted_product = find_product(text, predicted_label['vendor'], predicted_label['device_type'], products)
	if predicted_product is not '' and predicted_label['vendor'] is not '':
		print('Product Number: ', predicted_product)

main()
