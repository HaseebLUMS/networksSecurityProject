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
		print("Lines: ", lines)
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
	with open('new-unique-ips.json') as f: data = f.read()
	data = json.loads(data)
	ips = data['ips']

	import time
	s = time.perf_counter()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(asyncio.gather(*[scan(ip) for ip in ips[0:250]]))
	loop.close()
	elapsed = time.perf_counter() - s
	print(f"{__file__} executed in {elapsed:0.2f} seconds.")