import json
import os
import sys


with open("ips.txt") as f: ips = (f.read()).split("\n")
with open("censysTruth.json") as f: censys = json.loads(f.read())
with open("nmapTruth.json") as f: nmap = json.loads(f.read())


general = ['linux', 'mac', 'windows']


def is_gen(tmp):
	yes = False
	for ele in general:
		if ele in tmp:
			yes = True
	return yes


# m = {}
# for ip in ips:
# 	d = ""
# 	v = ""
# 	if ip in nmap:
# 		d = nmap[ip]["devices"]
# 		if len(d) > 0:
# 			d = d[0]

# 		vendors = []
# 		for tmp in nmap[ip]['os']:
# 			if not is_gen(tmp):
# 				vendors.append(tmp)
# 		for tmp in nmap[ip]['hw']:
# 			if not is_gen(tmp):
# 				vendors.append(tmp)
# 		tmp = {'ip':ip, 'device':d, 'vendor': vendors}
# 		newKey = len(m)
# 		m[newKey] = tmp

# print(m)
# m = json.dumps(m, indent=4)

# with open('mappNMAP.json', 'w') as f: f.write(m)



def flat(l):
	ans = ""
	for ele in l:
		ans += (ele + " - ")
	if len(ans) >= 3:
		if ans[-3:] == " - ":
			ans = ans[:-3]
	return ans


def trim(tag):
	tag = tag.split(",")[0].lower()
	if tag == 'network':
		tag = 'router'
	if 'router' in tag:
		tag = 'router'
	return tag



devices = {}
vendors = {}
products= {}
tuples  = {}

total = 0


mapp = {}


for ip in ips:
	d = ""
	v = ""
	p = ""

	if 'deviceType' in censys[ip]:
		device = censys[ip]['deviceType']
		device = trim(device)
		if device in devices:
			devices[device] += 1
		else:
			devices[device] = 1
		d = device

	if 'manufacturer' in censys[ip]:
		vendor = censys[ip]['manufacturer']
		vendor = trim(vendor)
		if vendor in vendors:
			vendors[vendor] += 1
		else:
			vendors[vendor] = 1
		v = vendor

	if 'product' in censys[ip]:
		product = censys[ip]['product']
		product = trim(product)
		if product in products:
			products[product] += 1
		else:
			products[product] = 1
		p = product


	tup = (d, v, p)

	if tup in tuples:
		tuples[tup] += 1
		total += 1
	else:
		tuples[tup] = 1
		total += 1

	tmp = {"ip": ip, "device_ztag": d, "vendor_ztag": v, "product_ztag": p}
	d = ""
	v = ""
	m = {}
	if ip in nmap:
		d = nmap[ip]["devices"]
		if len(d) > 0:
			d = d[0]
		else:
			d = " "

		vendors1 = []
		for tmp1 in nmap[ip]['os']:
			if not is_gen(tmp1):
				vendors1.append(tmp1)
		for tmp1 in nmap[ip]['hw']:
			if not is_gen(tmp1):
				vendors1.append(tmp1)
		tmp['device_nmap'] = d
		tmp['vendor_nmap'] = flat(vendors1)
		# tmp = {'ip':ip, 'device':d, 'vendor': vendors}
		# newKey = len(m)
		# m[newKey] = tmp
	try:
		with open('mappZTAG.json') as f: mapp = json.loads(f.read())
	except:
		mapp = {}
	newKey = len(mapp)
	mapp[newKey] = tmp
	mapp = json.dumps(mapp, indent=4)
	with open('mappZTAG.json', 'w') as f: f.write(mapp)

# print(vendors)

# for ele in products:
# 	print(products[ele])
# 	
print('Done')