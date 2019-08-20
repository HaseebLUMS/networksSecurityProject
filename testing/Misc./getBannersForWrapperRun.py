import json
with open('bannersFTP2.json') as f: data = f.read()
# with open('bannersTELNET.json') as f: data2 = f.read()
# data = data1 + data2
# print(data1[len(data1)-1])
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
with open('inputBanners2.json', 'w') as f: f.write(newData) 
