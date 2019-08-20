import json
with open('transactions.json') as f: data = f.read()
data = json.loads(data)
annons = set({})
for ele in data:
	annons.add(data[ele][1])
print(len(annons))