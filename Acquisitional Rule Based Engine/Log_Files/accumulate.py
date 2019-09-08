import json

HTTP = {}
for ele in range(0, 202):
	try:
		with open(str(ele)+'.json') as f: data = json.loads(f.read())
		HTTP[str(ele)] = data
	except:
		print(ele)
with open('_HTTP.json', 'w') as f: f.write(json.dumps(HTTP, indent=4))

