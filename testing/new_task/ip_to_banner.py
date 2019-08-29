import csv
import json
d = {}


def strip(word):
	if word[0] == "\"":
		word = word[1:]
	if word[-1] == "\"":
		word = word[0:-1]
	return word

def make_d(l):
	global d
	if len(l) < 1: return
	ip = l[0]
	banner = ""

	for i in range(1, len(l)):
		if l[i] == "" or l[i] == " ": continue
		word = strip(l[i])
		banner += (word + " ")
	if len(banner) < 1: return
	if banner[-1] == " ":
		banner = banner[0:-1]

	if len(banner) < 1: return
	if banner[-1] == 'n':
		banner = banner[0:-1]
	if ip in d:
		d[ip] = d[ip].append(banner)
	else:
		d[ip] = banner






with open('final_banners.csv') as f:
	file = csv.reader(f, delimiter=',')
	line_count = 0
	for row in file:
		if line_count == 0: 
			line_count += 1
			continue
		make_d(row[0:-6])
print(len(d))

with open('old_banners.json', 'w') as f: f.write(json.dumps(d, indent=4))

