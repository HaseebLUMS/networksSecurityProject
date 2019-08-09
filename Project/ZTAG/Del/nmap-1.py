import json
with open('nmapTruth.json') as f: data = f.read()

data = json.loads(data)

devs = 0
vends = 0
total = 0
for ele in data:
	total += 1
	if len(data[ele]['devices']) > 0: devs += 1
	tmp = data[ele]['os']
	len_tmp = len(tmp)
	if len_tmp > 0:

		for e in tmp:
			if 'linux' in e:
				len_tmp -= 1
			if 'windows' in e:
				len_tmp -= 1
	if len_tmp > 0:
		vends += len_tmp
print(devs, vends)
