import json
import os
import sys


with open("ips.txt") as f: ips = (f.read()).split("\n")
with open("censysTruth.json") as f: censys = json.loads(f.read())
with open("nmapTruth.json") as f: nmap = json.loads(f.read())



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

# print(vendors)

for ele in products:
	print(products[ele])