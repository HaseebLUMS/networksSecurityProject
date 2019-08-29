import json
from functools import reduce
import operator
with open('ref_banners.json') as f: banners = json.loads(f.read())
with open('foldedTrans.json') as f: trans = json.loads(f.read())

old_keys = trans.keys()
d = {}
print(len(banners))
count = 0
for ele in banners:
	ban = banners[ele]
	t = list(filter(lambda x: x in ban, old_keys))
	tt = list(map(lambda x: trans[x], t))
	# print(tt)
	try: anns = list(set(reduce(operator.concat, tt)))
	except: anns = []

	d[str(count)] = {"ip": ele, "refined banner": ban, "annotations": anns}
	# d[str(count)] = count
	count += 1

with open('annotations.json', 'w') as f: f.write(json.dumps(d, indent=4))