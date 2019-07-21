'''

Name: webcrawler.py
Argument: input.txt (a file containing banner data)
Output: A output.txt file which will contain data fetched 
		from google respective to banner data provided
		in input.txt.
How to run: python3 webcrawler.py input.txt
What does it do:
	--Reads input.txt and store it in "query" (a global variable)
	--Searches the Google for this query
	--Chooses top k search results (k is defined in config.py and can be toggled from there)
	--For every selected search result, extracts the data and cleans it.
	--Then stores it in output.txt
Dependecy: Requires Rake Library 
			See https://pypi.org/project/rake-nltk/
'''


from bs4 import BeautifulSoup
from googlesearch import search 
import time
from urllib.request import Request
from urllib.request import urlopen
import sys
import enchant
from rake_nltk import Rake
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
# sys.path.append('./../')
from config import page_limit
from headlessUser import perform_search
import re



query = ""
URLs = [] #Stores found URLs from google search relative to query
file = open(sys.argv[1])
query = file.read()
file.close()


'''
finds and stores URLS in list URLs defind above

Ignores URLs of popular sites (like social platforms) 
as they appear in search results on top but they are 
not useful.
'''
def find_urls(words):
	i = 10
	tmp_urls = []
	tmp_urls = perform_search(words)
	print(tmp_urls)

	
	trash = ['youtube.com', 'facebook.com', 'linkedin.com', 'twitter.com', 'quora.com', 'glassdoor.com', 'reddit.com', '.pdf', '.doc', '.docx']
	for url in tmp_urls:
		trashyURL = False
		for t in trash:
			if t in url: trashyURL = True
		if not trashyURL:
			URLs.append(url)





'''
Returns plain cleaned (by NLP texhniques) text data 

Goes to URLs found by function find_urls and extract text only
Then eliminates scripts or styles components from web text
Then does the necessary cleaning like back-slach n or back-slash r
And stores the output in file 'output.txt'
Steps:
	--kill all script and style elements
	--get text
	--break into lines and remove leading and trailing space on each
	--break multi-headlines into a line each
	--drop blank lines
	--Removes dictionary words
	--Extracts keywords
	--returns text (combination of keywords)
'''
def get_text(url):
	print(".")
	time.sleep(0.5)
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) #spoofed agent for avoiding scraping ban
	html = urlopen(req).read()
	soup = BeautifulSoup(html)
	for script in soup(["script", "style"]):
	    script.extract()
	text = soup.get_text()
	lines = (line.strip() for line in text.splitlines())
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	text = '\n'.join(chunk for chunk in chunks if chunk)

	return text




'''
Makes a output.txt
For every URL in URLs list, 
calls get_text() and stores in output.txt
'''
def create_output():
	global page_limit


	with open('raw.txt', 'w') as f:
		f.write(query)
	with open('output.txt', 'w') as f:
		f.write(query)


	for url in URLs:
		try:
			if page_limit > 0:
				text = get_text(url)
				with open('raw.txt', 'a+') as f:
					f.write("\n\n\n\n\n\n\n================= "+url + " ==================\n\n\n\n\n\n")
					f.write(text)

				with open('output.txt', 'a+') as f:
					text = refine_query(text, 2) #using the refining funtion
					f.write("\n\n\n\n\n\n\n================= "+url + " ==================\n\n\n\n\n\n")
					f.write(text)
					print(url, " : success")

					
			page_limit -= 1

		except:
			page_limit += 1
			if 'www.' not in url:
				URLs.append('www.' + url)
				print(url, " : queued for retry")
			else:
				print(url, " : url failed")

	return 1

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

The used regex is for eliminating
the html tags from the banner data
	--Second line of section 4.2, sub section "web crawler"
'''
def refine_query(q, mode):
	d = enchant.Dict('en_US')
	reg = re.compile('<.*?>')
	q = re.sub(reg, '', q)
	if mode == 1:
		q = q.replace('\\r', " ")
		q = q.replace('\\n', " ")
		q = q.replace("  ", " ")
	
	keywords = q.split(" ")
	possibleProd = find_pattern(q)
	
	r = Rake()
	r.extract_keywords_from_text(q)
	keywords = r.get_ranked_phrases()


	res = ""
	for kword in keywords:
		
		if kword is "": continue
		
		for k in kword.split(" "):

			if k is "": continue
			if (k is not "") and (d.check(k.lower()) == True) and (in_database(k.lower()) == False): continue
			
			if mode == 1:
				if k.isdigit() is True: continue
			
			res += (" " + k)
	
	for ele in possibleProd:
		if ele not in res:
			res += (" " + ele)
	return res


def count_words(l):
	count = 0
	for e in l:
		if len(e) > 2:
			count += 1
	return count


'''
Main function:
	--Finds all respective URLs (by find_urls())
	--shows the fetched URLs
	--Fetches the Text from URL sites and creates
	output.txt (by create_output())
'''
def main():
	global query
	res = refine_query(query, 1)
	res2= res.split(" ")
	res2 = count_words(res2)
	print('Query: ', res)
	with open('refinedQuery.txt', 'w') as file: file.write(res)

	if res2 > 1:
		find_urls(res)
		# for url in URLs: print(url)
		is_written = create_output()
	else:
		with open('raw.txt', 'w') as f:
			f.write("")
		
		with open('output.txt', 'w') as f:
			f.write(res)
		ans = ""
		for ele in res.split(" "):
			if ele is "": continue
			if in_database(ele) == True: ans += (" " + ele)
		with open('annotation.txt', 'w') as f: f.write(ans)


main()
