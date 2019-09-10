import json

FTP = {}
for ele in range(0, 85):
	try:
		with open(str(ele)+'.json') as f: data = json.loads(f.read())
		FTP[str(ele)] = data
	except:
		print(ele)
with open('_ferret.json', 'w') as f: f.write(json.dumps(FTP, indent=4))

