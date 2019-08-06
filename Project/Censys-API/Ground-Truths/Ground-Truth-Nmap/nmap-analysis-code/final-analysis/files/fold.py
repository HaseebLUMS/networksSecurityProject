import os
import sys
import glob
import json


files = glob.glob('*')
data = {}

for file in files:
	try:
		with open(file) as f: d = f.read()
		data[file] = d
	except:
		pass


data = json.dumps(data, indent=4)
with open('./../nmap-data.json', 'w') as f: f.write(data)