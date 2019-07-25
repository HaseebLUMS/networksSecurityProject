import json
import sys
import os

with open('banners.json') as f: data = f.read()

mapping = {}


data = json.loads(data)

ips = ['197.253.22.108']

for ele in data:
	ips.append(data[ele]["ip"])

print(ips)

myCmd = 'sudo nmap -sV -T4 '

for ip in ips:
	try:
		cmd = myCmd + str(ip)
		res = os.popen(cmd).read()
		print(res)
		lines = res.split('\n')
		ans = ''
		for l in lines:
			if 'Service Info' in l:
				ans = l
				break
		mapping[ip] = ans
		with open("mapping.json", 'w') as f:
			mapping2 = json.dumps(mapping, indent=4)
			f.write(mapping2)
	except:
		pass


