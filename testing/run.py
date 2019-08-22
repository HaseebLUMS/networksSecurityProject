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
import os
import sys
import json
import re
from rake_nltk import Rake
import enchant
# from "./mod_1_web_crawler_and_contexter/webcrawler" import main as crawler


''' writes state of execution in testing doc '''
def test_write(field, value):
	with open('1-testing.json') as f: data = json.loads(f.read())
	new_key = str(len(data)-1)
	data[new_key][field] = value
	data = json.dumps(data, indent=4)
	with open('1-testing.json', 'w') as f: f.write(data)


'''
Reads refined query written
by web crawler and return a list
'''
def refine_query(q, mode):
	with open('refinedQuery.txt', 'r') as file: data = file.read()
	return data



def write_query_map(ori, ref):
	with open("queryMap.json", "r") as f: prevData = f.read()
	prevData = json.loads(prevData)
	newKey = len(prevData)
	prevData[str(newKey)] = {"ori": ori, "ref": ref}
	prevData = json.dumps(prevData, indent=4)
	with open("queryMap.json", "w") as f: f.write(prevData)


anns = []
'''
Runs the ARE files sequenctially
'''
def run_files(ori):
	lps = {'pages':[]}
	lps = json.dumps(lps)
	with open('latest_pages.json', 'w') as f: f.write(lps)

	print('Prediction Engine Started!')
	comm = 'touch output.txt && rm output.txt'
	os.system(comm)

	move = False
	try:
		comm = 'python3 mod_1_web_crawler_and_contexter/webcrawler.py input_banner_data.txt mod_2_corpus_and_rule_based_der/Database/vendors mod_2_corpus_and_rule_based_der/Database/device_types make'
		os.system(comm)
		move = True
	except Exception as exception:
		print(exception)

	if move == False:
		return

	
	with open('refined_queries_set.json', 'r') as f: refined_queries = f.read()
	refined_queries = json.loads(refined_queries)
	refined_queries = refined_queries['queries']



	with open('intact_refined_query.txt') as f: intact_refined_query = f.read()
	test_write('refined banner', intact_refined_query)
	test_write('queries', refined_queries)


	pages = []
	for ref_que in refined_queries:
		write_query_map(ori, ref_que)
		print('in action: ', ref_que)
		with open('refinedQuery.txt', 'w') as f: f.write(ref_que)

		try:
			comm = 'python3 mod_1_web_crawler_and_contexter/webcrawler.py refinedQuery.txt mod_2_corpus_and_rule_based_der/Database/vendors mod_2_corpus_and_rule_based_der/Database/device_types run'
			os.system(comm)
			move = True
		except Exception as exception:
			move = False
			print("Exception occured in web crawler.", exception)


		with open('pages.json') as f: s_pages = json.loads(f.read())['pages']
		for ele in s_pages: pages.append(ele)

		with open('latest_pages.json') as f: latest_pages = json.loads(f.read())['pages']
		for ele in s_pages: latest_pages.append(ele)
		lps = {'pages': latest_pages}
		lps = json.dumps(lps, indent=4)
		with open('latest_pages.json', 'w') as f: f.write(lps)



		comm = 'touch mod_2_corpus_and_rule_based_der/Output/output.txt && rm mod_2_corpus_and_rule_based_der/Output/output.txt'
		os.system(comm)

		if move:
			comm = 'cp output.txt mod_2_corpus_and_rule_based_der/Output/output.txt'
			os.system(comm)
			comm = 'cp raw.txt mod_2_corpus_and_rule_based_der/raw.txt'
			os.system(comm)


		if move:
			try:
				comm = 'python3 mod_2_corpus_and_rule_based_der/NamedEntityRecognition.py mod_2_corpus_and_rule_based_der/Output/output.txt mod_2_corpus_and_rule_based_der/Database/vendors mod_2_corpus_and_rule_based_der/Database/device_types mod_2_corpus_and_rule_based_der/raw.txt'
				os.system(comm)
			except:
				move = False
				print("Exception occured in DER")

		

		
		comm = 'touch output.txt && rm output.txt'
		os.system(comm)

		with open("raw.txt", 'r') as f:
			data = f.read()
			data = data.split(" ")
			if len(data) < 3:
				move = False

		comm = 'cp raw.txt mod_3_local_dependency_finder/raw.txt && rm raw.txt'
		os.system(comm)

		
		comm = 'cp predictions.json mod_3_local_dependency_finder/predictions.json && rm predictions.json'
		os.system(comm)

		if move:
			try:
				comm = 'python mod_3_local_dependency_finder/local_dependency_finder.py mod_3_local_dependency_finder/predictions.json mod_3_local_dependency_finder/raw.txt'
				os.system(comm)
			except:
				print("Exception occured in local dependency finder")

		# if move is False:
		# 	with open('annotation.txt', 'w') as f:
		# 		f.write(" | | ")
		make_transaction()
	test_write('pages', pages)
	test_write('annotations', anns)
	return 1


'''
Makes a json file
of all transactions seen ever
for eventually being used for
generating rules by Apriori Algorithm
json format=> {1: [], 2:[], ..., n:[]}
'''

def make_transaction():
	global anns
	trans = ""
	with open('transactions.json', 'r') as fr: trans = fr.read()

	if len(trans) > 2: trans = json.loads(trans)
	else: trans = {}


	query = ''
	annotations = ''


	with open('input_banner_data.txt', 'r') as b: query = b.read()
	transaction = [refine_query(query, 1)]

	with open('annotation.txt', 'r') as a: annotations = a.read()
	for annotation in annotations.split("\n"):
		if annotation is "": continue
		anns.append(annotation)

		transaction2 = []
		for ele in transaction: transaction2.append(ele)

		transaction2.append(annotation)
		key = len(trans) + 1
		trans[(key)] = transaction2

	trans = json.dumps(trans, indent=4)
	with open('transactions.json', 'w+') as f: f.write(trans)



def main():
	with open('input_banner_data.txt') as f: data = f.read()

	heavy_servers = ['apache', 'iis', 'ngnix']
	data = data.lower()
	for ele in heavy_servers:
		if ele in data:
			print('banner belongs to nonIOT device.')
			return
	start = time.time()
	run_files(data)
	end = time.time()
	print('Execution Time: ', end - start)
main()


