import json
import csv

with open('ip_to_refined_banner.json') as f: ip_banner = json.loads(f.read())
with open('ip_to_truth.json') as f: ip_truth = json.loads(f.read())

def flat(truth):
	vendor = ""
	device = ""
	product = ""
	try: vendor = truth['manufacturer']
	except: pass
	try: device = truth['deviceType']
	except: pass
	try: vendor = truth['product']
	except: pass
	device = device.replace('network', 'router')
	return vendor + " | " + device + " | " + product

banner_to_truth = {}
for ele in ip_banner:
	ban = ip_banner[ele]
	truth = flat(ip_truth[ele])
	bans = ban.split(" ")
	for b in bans:
		banner_to_truth[b] = truth
def st_to_list(ann):
	ans = []
	tmp = ""
	st = False
	for ele in ann:
		if ele == "'":
			if st == False: st = True
			elif st == True: 
				ans.append(tmp)
				tmp = ""
				st = False
		elif st == True:
			tmp += ele
	return ans

def add_truth_to_row(row):
	ann = row[1]
	ann = st_to_list(ann)
	ban = ""
	for ele in ann:
		if ele.islower():
			ban = ele
			break
	truth = banner_to_truth[ban]
	# print(ban, truth)
	row.append(truth)
	return row

newFile = []
with open('Rules2.csv') as f:
	file = csv.reader(f, delimiter = ',')
	count = 0
	for row in file:
		if count == 0:
			row.append('Ground Truth')
			newFile.append(row)
			count += 1
			continue
		new_row = add_truth_to_row(row)
		newFile.append(new_row)
# print(newFile)


with open('rules2.csv', mode='w') as file:
	file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for ele in newFile:
		file_writer.writerow(ele)

