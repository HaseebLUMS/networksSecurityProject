import json

with open('ferretBanners.json') as f: data = json.loads(f.read())

zgrab = ""

for ele in data:
	tmp = {}
	tmp['ip'] = "115.42.162.129"
	tmp['timestamp_str'] = str('2019-08-04T22:16:09+05:00')
	tmp['data'] = {"upnp":{"banner":data[ele]['banner']}, "classification":"upnp", "success":1, "saddr":"115.42.162.129"}
	tmp['classification'] = "upnp"
	tmp['success'] = 1
	tmp['saddr'] = "115.42.162.129"

	tmp = json.dumps(tmp)
	zgrab += (tmp + "\n")

with open('ferretZGRAB.json', 'w') as f: f.write(zgrab)