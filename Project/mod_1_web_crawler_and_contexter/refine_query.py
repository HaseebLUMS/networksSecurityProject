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


# def is_date_time(k):
# 	db = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
# 	if k in db:
# 		return True
# 	return False


def remove_dates(data):
	db = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
	for ele in db:
		data = data.replace(ele, "")
	return data
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
	extra = ["(", ")", "{", "}", "[", "]", "!", "\"", "'", ","]
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


http_codes = ["100 Continue"
,"101 Switching Protocols"
,"200 OK"
,"201 Created"
,"202 Accepted"
,"203 Non-authoritative information"
,"204 no content"
,"205 reset content"
,"206 partial content"
,"300 multiple choices"
,"301 moved permanently"
,"302 found"
,"303 see other"
,"304 not modified"
,"305 use proxy"
,"306 (unused)"
,"307 temporary redirect"
,"400 bad request"
,"401 unauthorized"
,"402 payment required"
,"403 forbidden"
,"404 not found"
,"405 method not allowed"
,"406 not acceptable"
,"407 proxy authentication required"
,"408 request timeout"
,"409 conflict"
,"410 gone"
,"411 length required"
,"412 precondition failed"
,"413 request entity too large"
,"414 request-uri too long"
,"415 unsupported media type"
,"416 request range not satisfiable"
,"417 expectation failed"
,"500 internet server error"
,"501 not implemented"
,"502 bad gateway"
,"503 service unavailable"
,"504 gateway timeout"
,"505 http version not supported"]

def remove_http_codes(data, codes):
	data = data.lower()
	for code in codes:
		data = data.replace(code.lower(), "")
	data = data.replace("http/", "")
	return data

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

	q = remove_http_codes(q, http_codes)
	q = remove_dates(q)
	
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

	# if mode == 2:
	# 	r = Rake()
	# 	r.extract_keywords_from_text(q)
	# 	keywords = r.get_ranked_phrases()
	# else:
	# 	keywords = q.split(" ")


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
