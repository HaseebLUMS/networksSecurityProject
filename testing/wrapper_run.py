import json
import os


processedTransactions = {}

with open('inputBanners2.json') as b:
	data = b.read()
	data = json.loads(data)

banners = []
ips = []
for i in range(0, 200):
	try:
		tmp = data[str(i)]['banner']
		if 'filezilla' in tmp.lower(): continue
		if 'serve-u' in tmp.lower(): 
			continue
		banners.append(data[str(i)]['banner'])
		ips.append(data[str(i)]['ip'])
	except:
		pass

print(len(banners), len(ips))

def test_write_1(field, value):
	with open('1-testing.json') as f: data = json.loads(f.read())
	new_key = str(len(data))
	data[new_key] = {}
	data[new_key][field] = value
	data = json.dumps(data, indent=4)
	with open('1-testing.json', 'w') as f: f.write(data)


def test_write(field, value):
	with open('1-testing.json') as f: data = json.loads(f.read())
	new_key = str(len(data)-1)
	data[new_key][field] = value
	data = json.dumps(data, indent=4)
	with open('1-testing.json', 'w') as f: f.write(data)


for i in range(0, len(banners)):
	test_write_1('ip', ips[i])
	test_write('banner', banners[i])
	print("\n\n==================", i , "================\n\n")
	with open('input_banner_data.txt', 'w') as f:
		f.write(banners[i])
	comm = 'python run.py'
	try:
		os.system(comm)
	except:
		pass
