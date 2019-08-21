import json

with open('transactions.json') as f: data = json.loads(f.read())

def clean(k): return k.replace(" | ", " ")

def rm(li):
	ans = []
	for ele in li:
		if len(ele) >= 1:
			ans.append(ele)
	return ans


transactions = {}
counter = 0

for ele in data:
	tmp = data[ele]
	banners = rm(tmp[0].split(" "))
	annotations = rm(clean(tmp[1]).split(" "))

	for b in banners:
		for a in annotations:
			transactions[str(counter)] = [b,a]
			counter += 1

print(len(transactions), len(data))

with open('transactions2.json', 'w') as f: f.write(json.dumps(transactions, indent=4))
