import json
with open('tb.json') as f: data = f.read()
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
		if 'banner' in innerData['telnet']:
			banner = innerData['telnet']['banner']
		# elif 'ftp' in innerData:
		# 	banner = innerData['ftp']['banner']
			tmp = {'ip': ip, 'banner': banner}
			if len(banner) > 188: continue
			newData[str(count)] = tmp
			count += 1

print(len(newData))

newData = json.dumps(newData, indent=4)
with open('inputBanners4.json', 'w') as f: f.write(newData) 
