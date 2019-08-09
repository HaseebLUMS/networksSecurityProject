import json
with open('censysTruth.json') as f: data = f.read()
data = json.loads(data)

manu = 0
prod = 0
devi = 0

for ele in data:
	if 'product' in data[ele]: prod += 1
	if 'manufacturer' in data[ele]: manu += 1
	if 'deviceType' in data[ele]: devi += 1

print(manu, prod, devi)