from apyori import apriori
import json
import pandas as pd
import re
from rake_nltk import Rake

queries = ['MikroTik v5.24\r\nLogin:', '220 (vsFTPd 3.0.2)', 'BlackHole 3.0.5 vuzero\r\n\r\r\n\rvuzero login:', '220 MikroTik FTP server (MikroTik 5.16) ready', 'MikroTik v5.16\r\nLogin:', '220 kl.HalbichKutnohorska88 FTP server (MikroTik 6.42.4) ready', 'MikroTik v6.42.4 (stable)\r\nLogin:', '220 Phytoverse FTP server (MikroTik 6.44.1) ready', 'MikroTik v6.44.1 (stable)\r\nLogin:', '220 Ftp firmware update utility', 'ZyXEL VDSL Router\r\nLogin:', '220 mp-minsk-it-53.49 FTP server (MikroTik 5.25) ready', 'MikroTik v5.25\r\nLogin:', '220 UR5i FTP server (GNU inetutils 1.4.1) ready.', 'UR5i login:', '220 FTP service ready.', 'Login authentication\r\n\r\n\r\nUsername:', '220 FTP version 1.0', 'System administrator is connecting from 197.248.194.206\n\rReject the connection request !!!', '220 Ftp firmware update utility', 'BCM963268 Broadband Router\r\nLogin:', '220 FTP print service:V-1.13/Use the network password for the ID if updating.', '\x1b[2J\x1b[1;1f', '220-Microsoft FTP Service', '220-FileZilla Server version 0.9.36 beta\r\n220-written by Tim Kosse (Tim.Kosse@gmx.de)', '220 Ftp firmware update utility', 'BCM963268 Broadband Router\r\nLogin:', '220 MikroTik FTP server (MikroTik 6.39.2) ready', 'MikroTik v6.39.2 (stable)\r\nLogin:', '220 bftpd 2.2 at ::ffff:186.114.187.89 ready.', 'Login:', '220 (vsFTPd 2.2.2)', 'CentOS release 6.10 (Final)\r\nKernel 2.6.32-754.2.1.el6.x86_64 on an x86_64\r\nhm.sm.srv2196 login:', '220 MikroTik FTP server (MikroTik 6.43.2) ready', 'MikroTik v6.43.2 (stable)\r\nLogin:', '220 Hotspot Server FTP server (MikroTik 6.43.7) ready', 'MikroTik v6.43.7 (stable)\r\nLogin:', '220 Torre_Prefeitura FTP server (MikroTik 6.42.12) ready', 'MikroTik v6.42.12 (long-term)\r\nLogin:', '220 (vsFTPd 2.2.2)', 'SSH-2.0-OpenSSH_5.3', '220-Warning: Ftp is not a secure protocol, and it is recommended to use Sftp.\r\n220 FTP service ready.', "***********************************************************\r\n*           All rights reserved 2014-2016                 *\r\n*       Without the owner's prior written consent,        *\r\n* no decompiling or reverse-engineering shall be allowed. *\r\n* Notice:                                                 *\r\n*      This is a private communication system.            *\r\n*   Unauthorized access or use may lead to prosecution.   *\r\n***********************************************************\r\n\r\nWarning: Telnet is not a secure protocol, and it is recommended to use Stelnet. \r\n\r\nLogin authentication\r\n\r\n\r\nUsername:", '220 MikroTik FTP server (MikroTik 6.40.8) ready', 'MikroTik v6.40.8 (bugfix)\r\nLogin:', '220 BHXH_DongTrieu FTP server (Version 6.00LS) ready.', 'Wellcome BHXH Dong Trieu\r\n\r\x00\r\nBHXH_DongTrieu (ttypg)\r\x00\r\n\r\x00\r\nlogin:', '220 FTP Server Ready', '����\x00��\x01��"��\x03��\x03\r\nRemote Connection.\r\n\r\nUsername:', '220 bftpd 2.2 at 190.136.228.162 ready.']
# query = ['mikrotik', 'router']

score = 0
df = pd.read_pickle('RULES')
data = df['Items']
support = df['Support']
confidence = df['Confidence']

max_support = 0
max_confidence = 0
ans = {}


'''
While removing dictionary words,
it is checked that whether the target word
can be a vendor name or device name or not.
If yes, then it is not removed.
This functions just tells that the 
word can be a vendor or device name or not
'''
def in_database(word):
	with open(sys.argv[1]) as file: db1 = file.read()
	with open(sys.argv[2]) as file: db2 = file.read()

	return ((word in db1) or (word in db2))
'''
Product Regex is used here
because sometimes the product number
present in query is broken down by
refining libraries. With the help of this 
function, it will be prevented.
'''
def find_pattern(rawData):
	import re
	p = re.compile("[A-Za-z]+[-]?[A-Za-z]*[0-9]+[-]?[-]?[A-Za-z0-9]*\.?[0-9a-zA-Z]*")
	return p.findall(rawData)
'''
Uses Enchant library for removing dictionary words from 
input banner and extracting keywords. 

Uses Rake library for arranging words by their
rank (frequency) 
 -- useful when refining web page data
 -- reference = first para of Wen Crawler under 4.2

mode 1 for refining query
mode 2 for refining any other data
'''
def refine_query(q, mode):
	d = enchant.Dict('en_US')
	reg = re.compile('<.*?>')
	q = re.sub(reg, '', q)
	keywords = q
	possibleProd = find_pattern(q)
	r = Rake()
	r.extract_keywords_from_text(q)
	keywords = r.get_ranked_phrases()
	res = ""
	for kword in keywords:
		for k in kword.split(" "):
			if (k is not "") and (d.check(k) == True) and (in_database(k.lower()) == False):
				continue
			if mode == 1:
				if k.isdigit() is True:
					continue
			res += (" " + k)
	for ele in possibleProd:
		res += (" " + ele)
	return res


'''
Counts the number
of rules which do not
have predicted product number
'''
def countRulesWithoutProduct(rules):
	ans = 0
	for r in rules:
		tmp = 0
		for ele in r:
			for e in ele:
				if e == '|':
					tmp += 1
		if tmp == 2:
			ans += 1
	return [len(rules) - ans, len(rules)]

'''
Count overlap of query
with rule by counting number
of common keywords
'''
def countQueryELementsPresentInRule(rule, q):
	ans = 0
	for ele in rule:
		for eleQ in q:
			if ele.lower() == eleQ.lower():
				ans += 1
			elif eleQ.lower() in ele.lower():
				ans += 1
	return ans

'''
Given a set of rules
fins the rule with max overlap
'''
def findRuleWithMaxQueryOverlap(rules, query):
	ansNum = 0
	ansRule = {}
	ansConf = 0
	ansSup  = 0
	for r in range(0, len(rules)):
		tmp = countQueryELementsPresentInRule(rules[r], query)
		
		if tmp > ansNum and (support[r] > ansSup):
			ansNum = tmp
			ansRule = rules[r]
			ansConf = confidence[r]
			ansSup = support[r]

	return ansRule


'''
Given Banner data file,
returns predictions by ARE rules
'''
def main():
	num = countRulesWithoutProduct(data)
	print("Total Rules: ", num[1])
	print("Rules without product number: ", num[0])

	results = {}
	for query in queries:
		q = (refine_query(query, 1)).split(" ")
		ans = findRuleWithMaxQueryOverlap(data, q)
		for ele in ans:
			if " | " in ele:
				results[query] = ele
				print("Annotation: ", ele)

	results = json.dumps(results, indent=4)
	with open('results.json', 'w') as f:
		f.write(results)
main()