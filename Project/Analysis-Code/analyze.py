import json
data = {}

''' Loads ferret data'''
with open('ferret-23021-export (1).json') as f:
    data = json.load(f)


''' A little structuring'''
networks = list(data.keys())
try:
	networks.remove('messages')
	networks.remove('coolPeople')
except: pass
networksInfo = set()
for i in networks:
	meta	= list(data[i].keys())
	for m in meta: networksInfo.add(m)


#Structs
#{who} => HighSchool Kid
#{patching efforts} => attack, deviceIp, efforts, references, results
#{extendedPortsData} => [{ip, open ports}, ....]
#{NI} = ['extendedPortsData', 'patchingEfforts', 'who', 'paymentOption', 'newPaymentOption', 'data']


devs = ["0", "1"]
for i in range(1, 100):
	devs.append(str(i))
def filterDevices(a):
	if a in devs: return True
	else: return False


knownDevice   = 0
unknownDevice = 0
vulnerableDevices = 0
nv = 0
runsAsListNetworks = []



''' Collects Networks and Devices'''
for i in networks:
	if i == '25f4833e-eb35-41a6-96a7-a4e4d9793645':
		continue
	runs = list(data[i]['data'].keys())
	for r in runs:
		if (type(data[i]['data'][r]) is list):
			runsAsListNetworks.append(i)
			continue
		if r == "0":
			continue
		devices = list(data[i]['data'][r].keys())
		devices = filter(filterDevices, devices)
		for d in devices:
			host = data[i]['data'][r][d]['host']
			vul  = data[i]['data'][r][d]['vulnerable']
			if vul == True: vulnerableDevices += 1
			else: nv += 1 
			try:
				deviceName = host['deviceName']
				if deviceName != 'Unknown Name':
					# print deviceName
					knownDevice += 1
				else:
					unknownDevice += 1
			except:
				unknownDevice += 1

mahashes = set()
bannerMap = {}
entityMap = {}
for i in runsAsListNetworks:
	runs = list(data[i]['data'].keys())
	for r in runs:
		if r == "0": continue
		if type(data[i]['data'][r]) is not list:
			continue
		for di in data[i]['data'][r]:
			vul = di['vulnerable']
			if vul == True: vulnerableDevices += 1
			else: nv += 1
			try:
				mahashes.add(di['host']['mahash'])
				entityMap[di['host']['mahash']] = di
				# bannerMap[di['host']['mahash']] = di['vulnerabilityData']
			except:
				pass

			try:
				if di['host']['deviceName'] == 'Unknown Name':
					unknownDevice += 1
				else: knownDevice += 1
			except:
				unknownDevice += 1				




# A few of them are wrong Measures, only correct ones are used further 


print (len(entityMap))
print (len(mahashes))


j = 0
info = []

'''
builds deviceInfo.json

Reads the measures reported by above code 
and creates a clean JSON file which can be used for
analysis (the created file is used for banner analysis)
'''
for e in entityMap.values():
	if 'vulnerabilityData' in e:
		#do work here
		tmp = {}
		tmp['banner'] = []
		for b in e['vulnerabilityData']:
			if 'banner' in b:
				tmp['banner'].append(b['banner'])

		tmp['vendor'] = e['host']['vendor']
		tmp['mahash'] = e['host']['mahash']
		try:
			tmp['product']= e['host']['deviceName']
			if tmp['product'] == 'Unknown Name':
				tmp['product'] = 'null'
		except:
			tmp['product'] = 'null'
		info.append(tmp)
		j += 1

js = {'data': info}

with open("deviceInfo.json", "w") as file:
    json.dump(js, file, indent=4, sort_keys=True)
#113 unique devices
#22 unique vulnerabilities data


