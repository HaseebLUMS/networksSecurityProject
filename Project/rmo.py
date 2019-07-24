import json


def rmDup(s):
	sl = s.split(" ")
	newS = []
	for ele in sl:
		if ele == "": continue
		if ele.lower() not in newS:
			newS.append(ele.lower())
	ans = ""
	for ele in newS:
		ans += (ele + " ")
	return ans


with open("transactions.json") as f: data = f.read()

data = json.loads(data)

for i in range(1, 2261):
	data[str(i)][0] = rmDup(data[str(i)][0])

print(data)

data = json.dumps(data, indent=4)
with open("transactions.json", "w") as f: f.write(data)

