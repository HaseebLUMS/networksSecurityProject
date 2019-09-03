import json


bannersMap = {}
with open('inputBanners2.json') as f: b = f.read()
with open('inputBanners.json') as f: b0 = f.read()
b = json.loads(b)
b0 = json.loads(b0)
for ele in b:
	bannersMap[b[ele]['ip']] = b[ele]['banner']
for ele in b0:
	bannersMap[b0[ele]['ip']] = b0[ele]['banner']

def check(data):
	return data.replace("\n", "n")

with open('mappZTAG.json') as f: data = f.read()
data = json.loads(data)


ff = "IP,BANNER,ZTAG DEVICE,ZTAG VENDOR,ZTAG PRODUCT,NMAP DEVICE,NMAP VENDOR\n"

devices = set({})
vendors = set({})
products = set({})

for ele in data:
	tmp = ""
	ip = data[ele]['ip']
	
	ztag_device = " "
	ztag_vendor = " "
	ztag_product= " "
	nmap_device = " "
	nmap_vendor = " "
	banner      = " "

	try: ztag_device = data[ele]['device_ztag']
	except: pass
	try: ztag_vendor = data[ele]['vendor_ztag'] 
	except: pass
	try: ztag_product= data[ele]['product_ztag']
	except: pass
	try: nmap_device = data[ele]['device_nmap'] 
	except: pass
	try: nmap_vendor = data[ele]['vendor_nmap'] 
	except: pass
	try: banner = bannersMap[ip]
	except: pass

	# if nmap_device.lower() == " ":
	# 	devices.add(ztag_device)
	# if ztag_device.lower() == " ":
	# 	devices.add(nmap_device)
	# if (nmap_device.lower() != " ") and ztag_device.lower() in nmap_device.lower():
	# 	devices.add(nmap_device)
	# if ztag_vendor.lower() != " " or nmap_vendor.lower() == " ":
	# 	vendors.add(ztag_vendor)
	# if nmap_vendor.lower() != " ":
	# 	if nmap_vendor.lower() in ztag_vendor.lower():
	# 		vendors.add(nmap_vendor)
	# 	if ztag_vendor.lower() == " ":
	# 		vendors.add(nmap_vendor)
	products.add(ztag_product)

	banner = "\""+check(banner)+"\""
	tmp += (ip+','+banner+','+ztag_device+','+ztag_vendor+','+ztag_product+','+nmap_device+','+nmap_vendor + '\n')
	ff += tmp

# print(ff)
print(len(products))
with open('file_2.csv', 'w') as f: f.write(ff)