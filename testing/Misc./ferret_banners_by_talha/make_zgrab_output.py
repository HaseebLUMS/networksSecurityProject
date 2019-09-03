import json

with open('ferretBanners.json') as f: data = json.loads(f.read())

zgrab = ""

for ele in data:
	if 'http' in data[ele]['protocol'].lower():
		tmp = {}
		tmp['ip'] = "115.42.162.129"
		tmp['timestamp_str'] = str('2019-08-04T22:16:09+05:00')
		tmp['data'] = {"http":{"banner":data[ele]['banner']}, "success":1, "saddr":"115.42.162.129"}
		# tmp['classification'] = "upnp"
		tmp['success'] = 1
		tmp['saddr'] = "115.42.162.129"

		tmp = json.dumps(tmp)
		zgrab += (tmp + "\n")

with open('ferretZGRAB.json', 'w') as f: f.write(zgrab)