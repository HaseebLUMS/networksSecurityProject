import json

# with open('t2.json') as f: data = json.loads(f.read())
with open('type_2.json') as f: data = json.loads(f.read())


text = "IP,REFINED BANNER,ANNOTATIONS,TRANSACTIONS\n"

def check(data):

	data = data.replace("\n", " ")
	data = data.replace(",", " -- ")
	data = data.replace("\r", " ")
	data = data.replace("\t", " ")
	return data

def flat_list(l):
	ans = ""
	for e in l:
		ans += (e + " - ")
	if ans[-3:] == " - ":
		ans = ans[0:-3]
	return ans

def flat_list_double(l):
	l = str(l).replace(",", " - ")
	return l

for ele in data:
	tmp = data[ele]

	ip = " "
	banner = " "
	refined = " "
	queries = " "
	pages = " "
	annotations = " "
	transactions = " "

	try: ip = tmp['ip']
	except: pass


	try: banner = tmp['banner']
	except: pass


	try: refined = tmp['refined banner']
	except: pass


	try: queries = flat_list(tmp['queries'])
	except: pass


	try: pages = flat_list(tmp['pages'])
	except: pass


	try: annotations = flat_list(tmp['annotations'])
	except: pass


	try: transactions = flat_list_double(tmp['transactions'])
	except: pass
	banner = "'"+check(banner)+"'"


	t1 = ip + "," + refined + "," + annotations + "," + transactions + "\n"
	text += (t1)


with open('File_B2.csv', 'w') as f: f.write(text)