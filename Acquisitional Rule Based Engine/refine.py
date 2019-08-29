import re
import enchant
import sys
from combinations import generate_queries
from spellchecker import SpellChecker
spell = SpellChecker

'''
While removing dictionary words,
it is checked that whether the target word
can be a vendor name or device name or not.
If yes, then it is not removed.
This functions just tells that the 
word can be a vendor or device name or not
'''
def in_database(word, devices, vendors):
	word = word.lower()
	devices = list(map(lambda x: x.lower(), devices))
	vendors = list(map(lambda x: x.lower(), vendors))
	for d in devices:
		if d in word:
			return True
	for v in vendors:
		if v in word:
			return True
	return False


def remove_dates(data):
	data = data.lower()
	db = [' jan ', ' feb ', ' mar ', ' apr ', ' may ', ' jun ', ' jul ', ' aug ', ' sep ', ' oct ', ' nov ', ' dec ', ' sun ', ' mon ', ' tue ', ' wed ', ' thu ', ' fri ', ' sat ']
	for ele in db:
		data = data.replace(ele, " ")
	return data


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


def cut(upnp, token):
	ind_1 = upnp.find(token)
	if ind_1 == -1: return ""
	text = " "
	text = upnp[ind_1+len(token):]
	ind_1 = text.find('\r\n')
	if ind_1 == -1: ind_1 = len(text)-1
	text = text[0:ind_1]
	return text


def upnpRefine(upnp):
	server_part = ""
	server_token = "server:"
	st_part = ""
	st_token = "st:"
	usn_part = ""
	usn_token = "usn:"

	server_part = cut(upnp, server_token)
	st_part = cut(upnp, st_token)
	usn_part = cut(upnp, usn_token)

	server_part = server_part.replace(st_part, "")
	server_part = server_part.replace(usn_part, "")
	st_part = st_part.replace(usn_part, "")

	ans = server_part + " " + st_part + " " + usn_part
	ans = ans.replace('usn', '')
	ans = ans.replace('st', '')
	ans = ans.replace('  ', ' ')
	return ans


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

def refine_query(q, mode, devices, vendors):
	d = enchant.Dict('en_US')

	# if 'upnp' in q.lower():
	# q = upnpRefine(q.lower())

	q = remove_http_codes(q, http_codes)
	q = remove_dates(q)
	
	if mode == 1 or mode == 2: #Section 4.2, sub sec: Web Crawler, first para
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

		
		
	if mode == 1 or mode == 2:
		q = q.replace('\\r', " ")
		q = q.replace('\\n', " ")
		q = q.replace("  ", " ")
		q = q.replace('\r', " ")
		q = q.replace('\n', " ")
		q = q.replace("  ", " ")
	

	keywords = q.split(" ")
	res = ""
	for kword in keywords:
		if kword is "": continue
		for k in kword.split(" "):
			if k is "": continue
			k = trim(k)
			try:
				if (d.check(k.lower()) == True) and (in_database(k.lower(), devices, vendors) == False): continue
				# if len(spell.unknown([k.lower()])) == 0 and (in_database(k.lower(), devices, vendors) == False): continue
			except Exception as exception:
				# print("Exception: ", exception)
				pass
			if mode == 1 or mode == 2:
				if k.isdigit() is True: continue
			res += (" " + k)

				
	if mode == 2:
		return res.lower()
	
	if mode == 1:
		result = res.lower()
		result = generate_queries(result)
		return result


def refine_webpages_dictionary(url_to_page_dictionary):
	url_to_refined_page_dictionary = {}
	for url in url_to_page_dictionary:
		text = url_to_page_dictionary[url]
		refined_text = refine_query(text, 2, [], [])
		url_to_refined_page_dictionary[url] = refined_text
	return url_to_refined_page_dictionary

