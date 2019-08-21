import json

# with open('t2.json') as f: data = json.loads(f.read())
with open('1-testing.json') as f: data = json.loads(f.read())


text = "IP,BANNER,REFINED BANNER,SEARCH QUERIES,PAGES,ANNOTATIONS\n"

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


for ele in data:
	tmp = data[ele]

	ip = " "
	banner = " "
	refined = " "
	queries = " "
	pages = " "
	annotations = " "

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

	banner = "'"+check(banner)+"'"


	t1 = ip + "," + banner + "," + refined + "," + queries + "," + pages + "," + annotations + "\n"
	text += (t1)


with open('file2.csv', 'w') as f: f.write(text)