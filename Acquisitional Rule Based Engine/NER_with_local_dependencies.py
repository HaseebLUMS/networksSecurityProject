import re
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
	a = a.lower()
	b = b.lower()

	count = 0
	tmp = ""
	for t in text:

		if (a in t.lower()) and (b in t.lower()):
			for word in t.lower().split(" "):
				if a in word:
					tmp += 'v'
				if b in word:
					tmp += 'd'
			
			if('vd' in tmp):
				count += 1
				selected_text.append(t)
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
	# print(text, vendors, device_types)
	anns = [] #annotations	
	ans_ven = ''
	ans_dev = ''
	# print(vendors, device_types)
	for v in vendors:
		for d in device_types:
			count = count_related_lines(v, d, text)
			if count:
				ans_ven = v
				ans_dev = d
				anns.append({'vendor': ans_ven, 'device_type': ans_dev})
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
def find_product(sel_text, a, b, tags):
	text = sel_text
	ans_prod = set({})
	for t in tags:
		for line in text:
			try:
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
					if any_lower_ab == True:
						ans_prod.add(t.upper())
						# print(ans_prod)
						break
			except Exception as e:
				print('Exception in NER/find_product', e)
				pass
	return list(ans_prod)

'''
Finds product names by
matching possible candidates with
a regular expression
'''
def find_pattern(rawData):
	import re
	p = re.compile("[A-Za-z]+[-]?[A-Za-z]*[0-9]+[-]?[-]?[A-Za-z0-9]*\.?[0-9a-zA-Z]*")
	prods = p.findall(rawData)
	prods = list(filter(lambda x: len(x) < 10, prods))
	return prods



def find_annotations(banner, url_to_page_dictionary, devices, vendors):
	annotations = []
	pages_data = banner + " \n"
	for ele in url_to_page_dictionary:
		pages_data += (url_to_page_dictionary[ele] + " \n")
	tags = find_pattern(pages_data)
	pages_data = linefy_text(pages_data)
	partial_annotations = find_dependency(pages_data, vendors, devices)
	# print(partial_annotations)
	for ann in partial_annotations:
		v = ann['vendor']
		d = ann['device_type']
		print(ann)
		products = find_product(selected_text, v, d, tags)

		annotation_temp = v + " | " + d
		annotations.append(annotation_temp.upper())
		for p in products:
			annotation = annotation_temp + " | " + p
			annotations.append(annotation.upper())
	return annotations

