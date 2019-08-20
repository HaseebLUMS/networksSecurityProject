import json
with open('qa.json') as f: qa = f.read()
with open('qm.json') as f: qm = f.read()

with open('inputBanners.json') as f: b1 = f.read()
with open('inputBanners2.json') as f: b2 = f.read()

qa = json.loads(qa)
qm = json.loads(qm)
b1 = json.loads(b1)
b2 = json.loads(b2)


data = {}

for ele in b1:

	try:
		ip = b1[ele]['ip']
		banner = b1[ele]['banner']
		ref = qm[banner]

		data[ip] = ref
	except:
		pass


with open('ARE_IP_TO_REFINED_BANNER.json', 'w') as f: f.write(json.dumps(data,indent=4))