import json

FTP = {}
for ele in range(0, 372):
	try:
		with open(str(ele)+'.json') as f: data = json.loads(f.read())
		FTP[str(ele)] = data
	except:
		print(ele)
with open('_FTP.json', 'w') as f: f.write(json.dumps(FTP, indent=4))

