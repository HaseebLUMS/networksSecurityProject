import re
import enchant
from rake_nltk import Rake
import sys
from combinations import generate_queries


'''
While removing dictionary words,
it is checked that whether the target word
can be a vendor name or device name or not.
If yes, then it is not removed.
This functions just tells that the 
word can be a vendor or device name or not
'''
def in_database(word):
	with open(sys.argv[2]) as file: db1 = file.read()
	with open(sys.argv[3]) as file: db2 = file.read()

	return ((word.lower() in db1.lower().split("\n")) or (word.lower() in db2.lower().split("\n")))


def is_date_time(k):
	db = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
	if k in db:
		return True
	return False


'''
Product Regex is used here
because sometimes the product number
present in query is broken down by
refining libraries. With the help of this 
function, it will be prevented.
'''
def find_pattern(rawData):
	p = re.compile("[A-Za-z]+[-]?[A-Za-z]*[0-9]+[-]?[-]?[A-Za-z0-9]*\.?[0-9a-zA-Z]*")
	return p.findall(rawData)



def trim(k):
	f = False
	l = False
	extra = ["(", ")", "{", "}", "[", "]"]
	for ele in extra:
		if k[0] is ele:
			f = True
		if k[len(k)-1] is ele:
			l = True
	if f:
		k = k[1:]
	if l:
		k = k[:-1]
	return k


'''
Uses Enchant library for removing dictionary words from 
input banner and extracting keywords. 

Uses Rake library for arranging words by their
rank (frequency) 
 -- useful when refining web page data
 -- reference = first para of Wen Crawler under 4.2

mode 1 for refining query
mode 2 for refining any other data

The used regex is for eliminating
the html tags from the banner data
	--Second line of section 4.2, sub section "web crawler"
'''

def refine_query(q, mode):
	d = enchant.Dict('en_US')
	
	if mode == 1: #Section 4.2, sub sec: Web Crawler, first para
		pat_script = r"(?is)<script[^>]*>(.*?)</script>"
		q = re.sub(pat_script, "", q)


		pat_style = r"(?is)<style[^>]*>(.*?)</style>"
		q = re.sub(pat_style, "", q)


		pat_links = r'^https?:\/\/.*[\r\n]*'
		q = re.sub(pat_links, "", q)


		pat_links = r'^http?:\/\/.*[\r\n]*'
		q = re.sub(pat_links, "", q)


		reg = re.compile('<[^<]+?>')
		q = re.sub(reg, '', q)

		date_time = r'\d+[\/:\-]\d+[\/:\-\s]*[\dAaPpMn]*'
		q = re.sub(date_time, '', q)

		
		
	if mode == 1:
		q = q.replace('\\r', " ")
		q = q.replace('\\n', " ")
		q = q.replace("  ", " ")
	

	possibleProd = find_pattern(q)

	keywords = q.split(" ")

	if mode == 2:
		r = Rake()
		r.extract_keywords_from_text(q)
		keywords = r.get_ranked_phrases()
	else:
		keywords = q.split(" ")


	res = ""
	for kword in keywords:
		if kword is "": continue
		for k in kword.split(" "):
			k = trim(k)
			if k is "": continue
			try:
				if (d.check(k.lower()) == True) and (in_database(k.lower()) == False): continue
			except Exception as exception:
				print(exception)
				pass
			if mode == 1:
				if (k.isalpha() is False) and (k.isalnum() is False) and (k not in possibleProd): continue
				if k.isdigit() is True: continue
				if is_date_time(k) == True: continue
			res += (" " + k)
	

	if mode == 2:
		for ele in possibleProd:
			if ele not in res:
				res += (" " + ele)

				
	if mode == 2:
		return res.lower()
	if mode == 1:
		result = res.lower()
		result = generate_queries(result)
		return result
