import json
from make_transactions_functions import make_transactions_type_1
from make_transactions_functions import make_transactions_type_2
with open("1-testing.json") as f: data = json.loads(f.read())

data_1 = {}
data_2 = {}



for ele in data:
	try:
		if ele is "0": continue
		tmp = data[ele]
		try: banner = tmp['refined banner']
		except: banner = ""
		try: annotations = tmp['annotations']
		except: annotations = []

		#banner = "a b c d e f"
		#annotations = ["x | y | z", "xs", "1 | 2"]
		transactions2 = make_transactions_type_2(banner, annotations)
		data_2[ele] = data[ele].copy()
		data_2[ele]['transactions'] = transactions2
		
		transactions = make_transactions_type_1(banner, annotations)
		data_1[ele] = data[ele].copy()
		data_1[ele]['transactions'] = transactions
	except:
		pass

data_1 = json.dumps(data_1, indent=4)
data_2 = json.dumps(data_2, indent=4)

with open('type_1.json', 'w') as f: f.write(data_1)
with open('type_2.json', 'w') as f: f.write(data_2)