'''

Name: run.py
Argument: None
Output: Predicted Labels
How to run: python3 run.py
What does it do:
	Runs all the files required for 
	predicting the IoT labels.
	For description of these files, 
	please refer to individual files.
'''

import time
start = time.time()
import os
import sys
import json
from rake_nltk import Rake

def refine_query(q):
	r = Rake()
	r.extract_keywords_from_text(q)
	keywords = r.get_ranked_phrases()
	res = []
	for k in keywords:
		ks = k.split(' ')
		for eks in ks:
			res.append(eks)
	return res



comm = 'touch output.txt && rm output.txt'
res = os.popen(comm).read()
print('Prediction Engine Started!')

comm = 'python3 mod_1_web_crawler_and_contexter/webcrawler.py input_banner_data.txt'
res = os.popen(comm).read()
print(res)


comm = 'touch mod_2_corpus_and_rule_based_der/Output/output.txt && rm mod_2_corpus_and_rule_based_der/Output/output.txt'
res = os.popen(comm).read()


comm = 'cp output.txt mod_2_corpus_and_rule_based_der/Output/output.txt'
res = os.popen(comm).read()


comm = 'python3 mod_2_corpus_and_rule_based_der/NamedEntityRecognition.py mod_2_corpus_and_rule_based_der/Output/output.txt mod_2_corpus_and_rule_based_der/Database/vendors mod_2_corpus_and_rule_based_der/Database/device_types'
res = os.popen(comm).read()
print(res)

comm = 'touch output.txt && rm output.txt'
res = os.popen(comm).read()
# print(res)


comm = 'cp raw.txt mod_3_local_dependency_finder/raw.txt && rm raw.txt'
res = os.popen(comm).read()
# print(res)

comm = 'cp predictions.json mod_3_local_dependency_finder/predictions.json && rm predictions.json'
res = os.popen(comm).read()
# print(res)

print('Now Last Step....')
comm = 'python mod_3_local_dependency_finder/local_dependency_finder.py mod_3_local_dependency_finder/predictions.json mod_3_local_dependency_finder/raw.txt'
res = os.popen(comm).read()
print(res)

#{1: [], 2:[], ..., n:[]}
def make_transaction():
	
	trans = ""
	with open('transactions.json', 'r') as fr: trans = fr.read()
	if len(trans) > 2: trans = json.loads(trans)
	else: trans = {}
	query = ''
	annotation = ''
	with open('input_banner_data.txt', 'r') as b: query = b.read()
	transaction = refine_query(query)
	with open('annotation.txt', 'r') as a: annotation = a.read()
	transaction.append(annotation)
	key = len(trans) + 1
	trans[key] = transaction
	trans = json.dumps(trans, indent=4)
	with open('transactions.json', 'w+') as f: f.write(trans)
make_transaction()

end = time.time()
print('Execution Time: ', end - start)

