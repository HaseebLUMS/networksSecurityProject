import os
from pathlib import Path
query = [
"220 POLO SERVER FTP server (MikroTik 6.44.2) ready"
]



crawlerFiles = ['1.txt', '1m.txt', '2.txt', '2m.txt', '3.txt', '3m.txt', '4.txt', '4m.txt', '5.txt', '5m.txt', '6.txt', '6m.txt', '7.txt', '7m.txt', '8.txt', '8m.txt', '9.txt', '9m.txt', '10.txt', '10m.txt']
def clearCrawlerFiles():
	for f in crawlerFiles:
		os.system('touch '+ f)
		os.system('rm '+ f)




NERFiles = ['1 predictions.json', '2 predictions.json', '3 predictions.json','4 predictions.json', '5 predictions.json', '6 predictions.json', '7 predictions.json', '8 predictions.json', '9 predictions.json']
def clearNERFiles():
	for f in NERFiles:
		os.system('touch '+ f)
		os.system('rm '+ f)


def clearNERInputFiles():
	os.system('rm -r '+ 'mod_2_corpus_and_rule_based_der/Output')
	os.system('mkdir ' + 'mod_2_corpus_and_rule_based_der/Output/')

def runCrawler(q):
	clearCrawlerFiles()
	with open('input_banner_data.txt', 'w') as f:
		f.write(q)
	comm = 'python3 mod_1_web_crawler_and_contexter/webcrawler.py input_banner_data.txt'
	os.system(comm)



def runNER():
	clearNERFiles()
	clearNERInputFiles()

	tmp = []
	for f in crawlerFiles:
		file = Path(f)
		if file.exists() and 'm' in f: 
			tmp.append(f[0])
			name = 'mod_2_corpus_and_rule_based_der/Output/' + f
			os.system('cp ' + f + ' ' + name)

	for t in tmp:
		comm = 'python mod_2_corpus_and_rule_based_der/NamedEntityRecognition.py mod_2_corpus_and_rule_based_der/Output/'+t+'m.txt mod_2_corpus_and_rule_based_der/Database/vendors mod_2_corpus_and_rule_based_der/Database/device_types ' + t
		os.system(comm)



def writeToFile(f, q):

	with open(str(q) + '_test.txt', 'a+') as file:
		

		with open(f+'.txt') as file2:
			data = file2.read()
		file.write("Raw Data: \n")
		file.write(data)
		file.write('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')


		
		with open(f+'m.txt') as file3:
			data2 = file3.read()
		file.write("Refined Data: \n")
		file.write(data2)
		file.write('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')



		with open(f+' predictions.json') as file4:
			data3 = file4.read()
		file.write("NER Predictions: \n")
		file.write(data3)
		file.write('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')



		with open('annotation.txt') as file5:
			data4 = file5.read()
		file.write("Local Dependencies: \n")
		file.write(data4)
		file.write('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')


	print(f)


#local dependency finder
def runLDF(s):
	q = s
	with open(str(q) + '_test.txt', 'w') as file: file.write("")
	for f in crawlerFiles:
		file = Path(f)
		if file.exists() and ('m' not in f):
			comm = 'python mod_3_local_dependency_finder/local_dependency_finder.py ' + f[0] + '\ '+ 'predictions.json' + ' ' + f
			os.system(comm)

			writeToFile(f[0], q)


j = 1
for q in query:
	runCrawler(q)
	runNER()
	runLDF(j)
	j += 1
