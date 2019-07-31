import os
import json
import sys

devices = []
vendors = []


with open('clean-truths.json') as f: data = f.read()
data = json.loads(data)

def find_all(a_str, sub):
	start = 0
	while True:
		start = a_str.find(sub, start)
		if start == -1: return
		yield start
		start += len(sub)

def find(ch,string1):
	return list(find_all(string1, ch)) # [0, 5, 10, 15]

def findToken(token, info):
	pos = find(token, info)
	ans = []
	st = len(token)
	# token[info.find(token)] = '_'
	if 'Device: ' in token:
		for ele in pos:
			ans.append(info[(ele+st):].split(';')[0])
		# info = (info[st:]).split(';')[0]
	else:
		for ele in pos:
			ans.append(info[(ele+st):].split(', ')[0])
		# info = (info[st:]).split(' ')[0]
	return True, ans

for ele in data:
	info = data[ele]
	p, dev = findToken('Device: ', info)
	if p is True:
		for d in dev:
			devices.append(d)

	p, ven = findToken('cpe:/o:', info)
	if p is True:
		for v in ven:
			vendors.append(v)

	p, ven = findToken('cpe:/h:', info)
	if p is True:
		for v in ven:
			vendors.append(v)


devs = {}
for d in devices:
	if d not in devs:
		devs[d] = 1
	else:
		devs[d] += 1


vends = {}
for d in vendors:
	if d not in vends:
		vends[d] = 1
	else:
		vends[d] += 1

with open('analysis-Devices.json', 'w') as f:
	devs = json.dumps(devs, indent=4)
	f.write(devs)


with open('analysis-Vendors.json', 'w') as f:
	vends = json.dumps(vends, indent=4)
	f.write(vends)
