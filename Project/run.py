'''

Name: run.py
Argument: None
Output: Predicted Labels
How to run: python3 run.py
What does it do:
	Runs all the files required for 
	predicting the IoT labels.
	For description of these files, 
	please refer to "what run_dot_py does"
'''

import os
import sys


comm = 'touch output.txt && rm output.txt'
res = os.popen(comm).read()
print('Prediction Engine Started!')

print('First Step takes approximately 100 seconds')
comm = 'python3 mod_1_web_crawler_and_contexter/webcrawler.py input_banner_data.txt'
res = os.popen(comm).read()
print(res)
print('.\n.\n.\n.\n')


comm = 'touch mod_2_corpus_and_rule_based_der/Output/output.txt && rm mod_2_corpus_and_rule_based_der/Output/output.txt'
res = os.popen(comm).read()


comm = 'cp output.txt mod_2_corpus_and_rule_based_der/Output/output.txt'
res = os.popen(comm).read()


comm = 'touch mod_2_corpus_and_rule_based_der/Database/ind.json && rm mod_2_corpus_and_rule_based_der/Database/ind.json'
res = os.popen(comm).read()


comm = 'node mod_2_corpus_and_rule_based_der/index.js index mod_2_corpus_and_rule_based_der/Database/ind.json mod_2_corpus_and_rule_based_der/Output/'
res = os.popen(comm).read()
print(res)
print('.\n.\n.\n.\n')


comm = 'python3 mod_2_corpus_and_rule_based_der/find_device_info.py mod_2_corpus_and_rule_based_der/Database/vendors'
res = os.popen(comm).read()
print('Predicted Vendor Name ', res)


comm = 'python3 mod_2_corpus_and_rule_based_der/find_device_info.py mod_2_corpus_and_rule_based_der/Database/device_types'
res = os.popen(comm).read()
print('Predicted Device Type ', res)


comm = 'touch output.txt && rm output.txt'
res = os.popen(comm).read()
print('Done.')
