import json
with open('cleanBanners.json') as f: data = f.read()

data = data.split('\n')

count = 0

newData = {}
for i in range(0, len(data)-1):
	d = json.loads(data[i])
	ip = d['ip']
	innerData = d['data']
	banner = ''
	if 'telnet' in innerData:
		banner = innerData['telnet']['banner']
	elif 'ftp' in innerData:
		banner = innerData['ftp']['banner']
	tmp = {'ip': ip, 'banner': banner}
	newData[str(count)] = tmp
	count += 1

print(newData)

newData = json.dumps(newData, indent=4)
with open('inputBanners.json', 'w') as f: f.write(newData) 
