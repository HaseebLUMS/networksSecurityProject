import json

with open('newHTTP.json') as f: http = f.read()

http = http.split('\n{"ip"')
print(len(http))

entities = []
for ele in http:
	if not ele[0:5] == '{"ip"':
		entities.append('{"ip"' + ele)
print(len(entities))


bodies = []
for ele in entities:
	body = json.loads(ele)
	bodies.append(body)

banners = {}
count = 0
for ele in bodies:
	try:
		tmp = ele['data']['http']['response']['body']
		ip  = ele['ip']
		banners[str(count)] = {"ip":ip, "banner":tmp}
		count += 1
	except:
		pass


with open('httpBanners.json', 'w') as f: f.write(json.dumps(banners, indent=4))

