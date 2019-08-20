import json

with open('mappZTAG.json') as f: data = f.read()
data = json.loads(data)


ff = "IP,ZTAG DEVICE,ZTAG VENDOR,ZTAG PRODUCT,NMAP DEVICE,NMAP VENDOR\n"


for ele in data:
	tmp = ""
	ip = data[ele]['ip']
	
	ztag_device = " "
	ztag_vendor = " "
	ztag_product= " "
	nmap_device = " "
	nmap_vendor = " "

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

	tmp += (ip+','+ztag_device+','+ztag_vendor+','+ztag_product+','+nmap_device+','+nmap_vendor + '\n')
	ff += tmp

print(ff)

with open('file_1.csv', 'w') as f: f.write(ff)