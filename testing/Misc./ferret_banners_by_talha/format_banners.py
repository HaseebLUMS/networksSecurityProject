with open('ferretBanners.txt') as f: data = f.read()

data = data.replace("\"", " ")
data = data.replace("u\'", "\'")
data = data.replace("\'", "\"")

data = data.split("\n")

import json



ferretBanners = {}
count = 0
for record in data:
	try:
		record = json.loads(record)
		ferretBanners[str(count)] = {'ip':count, 'banner': record['banner'], 'deviceInfo': record['deviceInfo']}
		count += 1
	except:
		print(record)
		pass

with open('ferretBanners.json', 'w') as f: f.write(json.dumps(ferretBanners, indent=4))