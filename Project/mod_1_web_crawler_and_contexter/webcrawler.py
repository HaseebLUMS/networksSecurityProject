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
from rake_nltk import Rake
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
# sys.path.append('./../')
from config import page_limit
from headlessUser import performSearch


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

def findURLs(words):
	i = 10
	tmp_urls = []
	# for j in search(words,num=page_limit, start=0, stop=page_limit, pause=1): 
	# 	time.sleep(2)
	# 	tmp_urls.append(j)
	tmp_urls = performSearch(words)

	trash = ['youtube.com', 'facebook.com', 'linkedin.com', 'twitter.com', 'quora.com', 'glassdoor.com', 'reddit.com', '.pdf', '.doc', '.docx']
	for url in tmp_urls:
		trashyURL = False
		for t in trash:
			if t in url: trashyURL = True
		if not trashyURL:
			URLs.append(url)





'''
Returns plain cleaned (by NLP texhniques) text data 

Goes to URLs found by function findURLs and extract text only
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
def getText(url):
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
	# r = Rake()
	# r.extract_keywords_from_text(text)
	# keywords = r.get_ranked_phrases()
	# res = ""
	# for k in keywords:
	# 	res += (" " + k)
	# return res




'''
Makes a output.txt
For every URL in URLs list, 
calls getText() and stores in output.txt
'''
def create_output():
	global page_limit
	pages_searched = 0
	with open('output.txt', 'w') as f:
		tmp = 'For query: ' + query
		f.write(tmp)
	for url in URLs:
		try:
			if page_limit:
				text = getText(url)
				with open('raw.txt', 'a+') as f:
					tmp = '\n==============='+ url+ '================\n'
					f.write(tmp)
					pages_searched += 1
					# print(url, " : success")
					f.write(text)

				with open('output.txt', 'a+') as f:
					r = Rake()
					r.extract_keywords_from_text(text)
					keywords = r.get_ranked_phrases()
					res = ""
					for k in keywords:
						res += (" " + k)
					text = res
					tmp = '\n==============='+ url+ '================\n'
					f.write(tmp)
					# pages_searched = 1
					print(url, " : success")
					f.write(text)

					
			page_limit -= 1

			time.sleep(2)
		except:
			print(url, " : failed")
			time.sleep(1)
	return 1


'''
Uses Rake library for removing dictionary words from 
input banner and extracting keywords. 
'''
def refine_query(q):
	r = Rake()
	r.extract_keywords_from_text(q)
	keywords = r.get_ranked_phrases()
	res = ""
	for k in keywords:
		res += (" " + k)
	print("Refined Formated Query: ", res)
	return res


'''
Main function:
	--Finds all respective URLs (by findURLs())
	--shows the fetched URLs
	--Fetches the Text from URL sites and creates
	output.txt (by create_output())
'''
def main():
	global query
	res = refine_query(query)
	findURLs(res)
	# for url in URLs: print(url)
	is_written = create_output()
	if is_written:
		print('\nOutput Successfully created by web crawler')

main()
