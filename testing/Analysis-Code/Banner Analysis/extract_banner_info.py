import json



'''
Uses deviceInfo.json and extracts 
relevant banners
'''

data = {}
with open('deviceInfo.json') as f:
	data = json.load(f)
data = data["data"]
UPNPs = []
SSHs  = []
vendors = []


#Code for formatting the data to a minimal dictionary is in analyze.py
#deviceInfo.json is made by analyze.py and used here
for d in data:
	bl = d['banner']
	for l in bl:
		if l['protocol'] == 'UPNP':
			UPNPs.append(l['text'])
		if l['protocol'] == 'SSH':
			SSHs.append(l['text'])
	v  = d['vendor']
	vendors.append(v)


for i in vendors:
	print(i)
for i in UPNPs:
	print(i)
for i in SSHs:
	print(i)
