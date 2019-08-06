import json
import sys
import os
import asyncio

async def scan(ip):
	try:
		print(ip, ' started...')
		# myCmd = 'sudo nmap -sV -T4 '
		# cmd = myCmd + str(ip)
		res = await asyncio.create_subprocess_shell('sudo nmap -sV -T4 '+str(ip), stdout=asyncio.subprocess.PIPE)
		stdout, err = await res.communicate()
		res = ''
		if stdout: res = stdout.decode()
		print("==>", res)
		lines = str(res).split('\n')
		# print("Lines: ", lines)
		ans = 'Unknown'
		for l in lines:
			if 'Service Info' in l:
				ans = l
				break
		with open('./files/'+ip, 'w') as f:
			f.write(ans)
	except:
		pass


if __name__ == "__main__":
	with open('inputBanners.json') as f: data = f.read()
	with open('inputBanners2.json') as f: data2 = f.read()
	data = json.loads(data)
	data2 = json.loads(data2)
	ips = []
	for ele in data:
		ips.append(data[ele]['ip'])
	for ele in data2:
		ips.append(data2[ele]['ip'])
	print(len(ips))
	# ips = data['ips']

	import time
	s = time.perf_counter()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(asyncio.gather(*[scan(ip) for ip in ips[0:500]]))
	loop.close()
	elapsed = time.perf_counter() - s
	print(f"{__file__} executed in {elapsed:0.2f} seconds.")