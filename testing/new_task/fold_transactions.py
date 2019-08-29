import json

with open('transactions.json') as f: data = f.read()
data = json.loads(data)

d = {}

for ele in data:
	tmp = data[ele]
	if tmp[0] in d:
		d[tmp[0]].append(tmp[1].upper())
	else:
		d[tmp[0]] = [tmp[1].upper()]

for ele in d:
	d[ele] = list(set(d[ele]))

with open('foldedTrans.json', 'w') as f: f.write(json.dumps(d, indent=4))