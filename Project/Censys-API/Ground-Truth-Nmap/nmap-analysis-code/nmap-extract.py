import os
import sys
import json

with open('ip-wise-ground-truths.json') as f: data = f.read()
data = json.loads(data)


OS = {'cisco:ios', 'apc:aos', 'adtran:aos', 'huawei:vrp', 
	'mikrotik:routeros', 'zyxel:zynos', 'freebsd:freebsd', 
	'acme:micro_httpd', 'windriver:vxworks', 'hp:comware:5.20.106'}


def fold(li):
	folded_list = ""
	for i in range(0, len(li)-1):
		folded_list += (li[i] + ' | ')
	folded_list += (li[len(li)-1])
	return folded_list

def manu():
	manufacturers = {}
	for ele in data:
		manus = ""
		if len(data[ele]['hw']) > 0:
			manus = fold(data[ele]['hw'])
			manus += " | "
		if len(data[ele]['os']) > 0:
			for o in data[ele]['os']:
				if o in OS:
					manus += (o + ' | ')
		if len(manus) > 0:
			if manus[-3:] == ' | ': 
				manus = manus[0: len(manus)-3]
			manufacturers[ele] = manus
	print(len(manufacturers))
	manufacturers = json.dumps(manufacturers, indent=4, sort_keys=True)
	with open('nmap-manufacturers.json', 'w') as f: f.write(manufacturers)

def uniqueOS():
	os = set({})
	for ele in data:
		for o in data[ele]['os']:
			os.add(o)
	print(os)


def dev():
	devices = {}
	for ele in data:
		if len(data[ele]['devices']) > 0:
			devices[ele] = fold(data[ele]['devices'])
	print(len(devices))
	devices = json.dumps(devices, indent=4, sort_keys=True)
	with open('nmap-devices.json', 'w') as f: f.write(devices)

manu()