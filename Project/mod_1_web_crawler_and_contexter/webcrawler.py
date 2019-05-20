from bs4 import BeautifulSoup
from googlesearch import search 
import time
from urllib.request import Request
from urllib.request import urlopen

query = "220 Welcome to ASUS RT-AC58U FTP service \r\n"



URLs = []

'''
finds and stores URLS in list URLs defind above

Ignores URLs of popular sites (like social platforms) 
as they appear in search results on top but they are 
not useful.
'''
def findURLs(words):
	i = 10
	tmp_urls = []
	for j in search(words,num=15, start=0, stop=15, pause=5): 
		time.sleep(2)
		tmp_urls.append(j)

	trash = ['youtube.com', 'facebook.com', 'linkedin.com', 'twitter.com', 'quora.com', 'glassdoor.com', 'reddit.com', '.pdf', '.doc']
	for url in tmp_urls:
		trashyURL = False
		for t in trash:
			if t in url: trashyURL = True
		if not trashyURL:
			URLs.append(url)
findURLs(query)


for url in URLs: print(url)


'''
Returns plain cleaned text data

Goes to URLs found by function findURLs and extract text only
Then eliminates scripts or styles components from web text
Then does the necessary cleaning like back-slach n or back-slash r
And stores the output in file 'output.txt'
'''
def getText(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) #spoofed agent for avoiding scraping ban
	html = urlopen(req).read()
	soup = BeautifulSoup(html)


	# kill all script and style elements
	for script in soup(["script", "style"]):
	    script.extract()    # rip it out
	# get text
	text = soup.get_text()
	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)
	return text


i = 10
with open('output.txt', 'a+') as f:
	tmp = 'For query: ' + query
	f.write(tmp)
for url in URLs:
	try:
		if i:
			text = getText(url)
			with open('output.txt', 'a+') as f:
				tmp = '\n==============='+ url+ '================\n'
				f.write(tmp)
				f.write(text)
		i -= 1

		time.sleep(2)
	except:
		time.sleep(1)
