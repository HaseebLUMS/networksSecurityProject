import json



tag = 'telnet'
banners = set({})

with open('banners.json') as f: data = f.read()
newData = ''
data = data.split('\n')

for rec in data:
	try:
		d = json.loads(rec)
		if len(d['data']) > 0:
			if len(d['data'][tag]) > 0:
				if d['data'][tag]['banner'] not in banners:
					banners.add(d['data'][tag]['banner'])
					newData += (json.dumps(d) + '\n')
	except:
		pass

print(newData)


with open('cleanBanners.json', 'a+') as f: f.write(newData)

