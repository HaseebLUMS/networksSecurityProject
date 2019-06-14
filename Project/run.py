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