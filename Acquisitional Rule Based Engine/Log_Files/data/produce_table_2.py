import json

with open('_ferret.json') as f: data = json.loads(f.read())

# "pipeline_numbers": {
#     "ner_devs": 0,
#     "ner_vends": 0,
#     "ner_prods": 0,
#     "ld_dv": 0,
#     "ld_dvp": 0
# }

def find_root(ele):
	if 'pipeline_numbers' in data[ele]:
		return ele
	elif 'num' in data[ele]:
		return find_root(str(data[ele]['num']))
	# else:
	# 	return "0"
ner_devs = 0
ner_vends = 0
ner_prods = 0
ld_dv = 0
ld_dvp = 0

for ele in data:
	# try:
	tmp = None
	# if 'pipeline_numbers' in data[ele]:
	# 	tmp = data[ele]['pipeline_numbers']
	# elif 'num' in data[ele]:
	# 	tmp = data[str(data[ele]['num'])]['pipeline_numbers']
	num = find_root(ele)
	# if num is None: print(ele)
	tmp = data[num]['pipeline_numbers']

	if tmp["ner_devs"] > 0:
		ner_devs += 1
	if tmp["ner_vends"] > 0:
		ner_vends += 1
	if tmp["ner_prods"] > 0:
		ner_prods += 1
	if tmp["ld_dv"] > 0:
		ld_dv += 1
	if tmp["ld_dvp"] > 0:
		ld_dvp += 1
	# except:
	# 	print(ele)
print(ner_devs, ner_vends, ner_prods, ld_dv, ld_dvp)