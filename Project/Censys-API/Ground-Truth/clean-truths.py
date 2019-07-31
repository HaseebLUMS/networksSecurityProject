import os
import json
import sys

with open('files/nmap-data.json') as f: data = f.read()
data = json.loads(data)

newData = {}

for ele in data:
	if 'Unknown' in data[ele]: continue
	else: newData[ele] = data[ele] 

print(newData)
newData = json.dumps(newData, indent=4)
with open('clean-truths.json', 'w') as f: f.write(newData)