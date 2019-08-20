import json
with open('cleanBanners.json') as f: data = f.read()
data = data.split('\n')

ips = []
for ele in data:
	if len(ele) > 1:
		tmp = json.loads(ele)
		ips.append(tmp['ip'])

print(ips)
d = {'ips':ips}
d = json.dumps(d, indent=4)
with open('./../Censys-API/Ground-Truths/Ground-Truth-Nmap/nmap-analysis-code/final-analysis/new-unique-ips.json', 'w') as f: f.write(d)

