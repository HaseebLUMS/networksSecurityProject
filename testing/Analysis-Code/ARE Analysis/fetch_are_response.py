import os 
import sys
import json
data = {}
with open('deviceInfo.json') as f:
	data = json.load(f)

''' a little cleaning '''
def clean(text):
	text = text.replace('\r', '')
	text = text.replace('\n', '')
	return text



'''
Queries ARI API

Uses the file deviceInfo.json and run the curl command 
for queryinh ARE API
'''
data = data["data"]
results = []
for d in data:
	banner = d['banner']
	for b in banner:
		try:
			TYPE = b['protocol']
			DATA = clean(b['text'])

			# TYPE = "FTP"
			# DATA = "220 Welcome to ASUS RT-AC58U FTP service."
			comm = 'curl -X POST -H "Content-Type: application/json" -d \'{"type": "'+ TYPE + '", "b_data": "' + DATA + '"}\' http://are1.tech:5000/tag'
			res = os.popen(comm).read()
			results.append(res)
		except:
			pass


print(results)
#EVERY REQUESTS RESULTS IN EITHER "ERROR" OR "BAD REQUEST", 
#0 ANSWERS
#0 Correctly labeled devices