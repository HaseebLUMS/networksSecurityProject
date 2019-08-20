import os
import sys
import re
import json


#Classes of Local Dependencies
A = 'V.D.P'
B = 'VDP'
C = 'VD.P'
D = 'VP.D'
E = 'VPD'
classes = [A, B, C, D, E]

#takes text as input and identify all the places
#where vendor, device or product is present
#....
#for "ASUS is good" returns "<ASUS, vendor> is good"
def makeSequence(text, setVendors, setDevices, setProducts):
	sequence = []
	text = text.replace("\n", " ")
	text = text.replace("  ", " ")
	for ele in text.split(' '):
		if ele in setVendors:
			sequence.append({'vendor': ele})
		elif ele in setProducts:
			sequence.append({'product': ele})
		elif ele in setDevices:
			sequence.append({'device': ele})
		else:
			sequence.append({'...': ele})
	# print(sequence)
	return sequence



#trims starting and ending dots
def trim(data):
	ans = ""
	for i in range(0, len(data)):
		if (i == 0) and (data[i] == '.'):
			continue
		if (i == len(data)-1) and (data[i] == '.'):
			continue
		ans += data[i]
	return ans



#finds local dependency pattern in input "sequence"
def findLP(sequence):
	ans = []
	tmp = ""
	v = "" 
	p = ""
	d = ""
	for i in range(0, len(sequence)):
		if i == len(sequence)-1:
			ans.append([trim(tmp), v, d, p])
		ele = sequence[i]
		if 'vendor' in ele:
			ans.append([trim(tmp), v, d, p])
			tmp = ""
			if len(ans) > 0:
				tmp += '.V'
				v = ele['vendor']
			else:
				tmp += 'V'
				v = ele['vendor']
		elif 'product' in ele:
			tmp += 'P'
			p = ele['product']
		elif 'device' in ele:
			tmp += 'D'
			d = ele['device']
		else:
			if len(tmp) == 0:
				tmp += '.'
			elif not (tmp[len(tmp)-1] == '.'):
				tmp += '.'


	return ans


def readFilesAndRun():


	# text = '''A mikrotik router is very XN-10 is a good thing.'''
	with open(sys.argv[2], 'r') as f: text = f.read()
	
	with open(sys.argv[1], 'r') as f: predictions = json.loads(f.read())
	vendors = predictions['vendors']
	device_types = predictions['device_types']
	products = predictions['products']
	

	for p in products:
		for d in device_types: 
			for v in vendors:
				setVendors = {v.lower()}
				setDevices = {d.lower()}
				setProducts = {p.lower()}
				sequence = makeSequence(text.lower(), setVendors, setDevices, setProducts)
				ans = findLP(sequence)
				for ele in ans:
					if ele[0] in classes:
						return ele


def main():
	print(readFilesAndRun())

main()