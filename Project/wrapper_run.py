import json
import os


processedTransactions = {}

with open('inputBanners.json') as b:
    data = b.read()
    data = json.loads(data)

banners = []
for i in range(500, 1000):
	try:
	    banners.append(data[str(i)]['banner'])
	except:
		pass

print(len(banners))

for i in range(0, len(banners)):
	print("\n\n==================", i , "================\n\n")
	with open('input_banner_data.txt', 'w') as f:
		f.write(banners[i])
	comm = 'python run.py'
	try:
		os.system(comm)
	except:
		pass
