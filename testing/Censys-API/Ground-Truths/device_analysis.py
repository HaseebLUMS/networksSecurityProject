import os
import sys
import json

with open('./Ground-Truth-Nmap/nmap-devices.json') as f: nmap = json.loads(f.read())
with open('./Ground-Truth-Censys/censys-devices.json') as f: censys = json.loads(f.read())


for ele in censys:
	if censys[ele].lower() == 'network':
		censys[ele] = 'router'
	if 'router' in censys[ele].lower():
		censys[ele] = 'router'

for ele in nmap:
	if nmap[ele].lower() == 'network':
		nmap[ele] = 'router'
	if 'router' in nmap[ele].lower():
		nmap[ele] = 'router'

true = 0
trueSet = {}
false = 0
falseSet = {}
unknown = 0
unknownSet = {}

for ele in nmap:
	if ele in censys:
		if censys[ele].lower() in nmap[ele].lower():
			true += 1
			if censys[ele].lower() in trueSet: trueSet[censys[ele].lower()] += 1
			else: trueSet[censys[ele].lower()] = 1
			# trueSet.add(censys[ele].lower())
		else:
			false += 1
			if censys[ele].lower() in falseSet: falseSet[censys[ele].lower()] += 1
			else: falseSet[censys[ele].lower()] = 1
			# falseSet.add(censys[ele].lower())
	else:
		unknown += 1
		if nmap[ele].lower() in unknownSet: unknownSet[nmap[ele].lower()] += 1
		else: unknownSet[nmap[ele].lower()] = 1
		# unknownSet.add(nmap[ele].lower().split(":")[0])

runknown = 0
runknownSet = {}
for ele in censys:
	if ele not in nmap:
		runknown += 1
		if censys[ele].lower() in runknownSet: runknownSet[censys[ele].lower()] += 1
		else: runknownSet[censys[ele].lower()] = 1

# print("True: ", true, "\nFalse: ", false, "\nUnknown: ", unknown)
# print("\n")
# print("True: \n", trueSet, "\n\nFalse: \n", falseSet, "\n\nUnknown: \n", unknownSet)

manufacturers_analysis = {}
manufacturers_analysis['annotated by nmap out of 1000'] = len(nmap)
manufacturers_analysis['annotated by censys out of 1000'] = len(censys)
manufacturers_analysis['True in nmap checked against censys'] = {'total':true, 'names': trueSet}
manufacturers_analysis['False in nmap checked against censys'] = {'total':false, 'names': falseSet}
manufacturers_analysis['In nmap but unknown by censys'] = {'total':unknown, 'names': unknownSet}
manufacturers_analysis['In censys but unknown by nmap'] = {'total':runknown, 'names': runknownSet}
print(manufacturers_analysis)
manufacturers_analysis = json.dumps(manufacturers_analysis, indent=4)
with open('device-analysis-of-nmap-against-censys.json', 'w') as f: f.write(manufacturers_analysis)