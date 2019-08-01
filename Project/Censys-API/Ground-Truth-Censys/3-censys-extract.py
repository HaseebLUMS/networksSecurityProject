import os
import sys
import json

def manu():
	with open('metadata.json') as f: data = f.read()
	data = json.loads(data)

	manufacturers = {}
	for ele in data:
		try:
			manufacturers[ele] = data[ele]['metadata.manufacturer']
		except:
			pass

	print(len(manufacturers))

	manufacturers = json.dumps(manufacturers, indent=4, sort_keys=True)
	with open('censys-manufacturers.json', 'w') as f: f.write(manufacturers)

def dev():
	with open('metadata.json') as f: data = f.read()
	data = json.loads(data)

	devices = {}
	for ele in data:
		try:
			devices[ele] = data[ele]['metadata.device_type']
		except:
			pass

	print(len(devices))

	devices = json.dumps(devices, indent=4, sort_keys=True)
	with open('censys-devices.json', 'w') as f: f.write(devices)

manu()