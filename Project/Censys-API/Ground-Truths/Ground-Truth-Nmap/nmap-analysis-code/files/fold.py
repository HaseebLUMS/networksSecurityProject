import os
import sys
import glob
import json


files = glob.glob('*')
data = {}

for file in files:
	with open(file) as f: d = f.read()
	data[file] = d


data = json.dumps(data, indent=4)
with open('./../nmap-data.json', 'w') as f: f.write(data)