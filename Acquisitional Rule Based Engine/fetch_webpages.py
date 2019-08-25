from bs4 import BeautifulSoup
from urllib.request import Request
from urllib.request import urlopen
import sys
import warnings
if not sys.warnoptions: warnings.simplefilter("ignore")
import multiprocessing
import time

def get_text(url, return_dict):
	try:
		time.sleep(1)
		req = Request(url, headers={'User-Agent': 'Mozilla/4.0'})
		html = urlopen(req).read()
		soup = BeautifulSoup(html)
		for script in soup(["script", "style"]):
			script.extract()
		text = soup.get_text()
		lines = (line.strip() for line in text.splitlines())
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		text = '\n'.join(chunk for chunk in chunks if chunk)
		return_dict['text'] = text
		return text
	except Exception as e:
		print("Error in fetch_webpages/get_text ", url, e)
		return



def page_search(url):
	try:
		manager = multiprocessing.Manager()
		return_dict = manager.dict()
		return_dict['text'] = url
		text = ''
		p = multiprocessing.Process(target=get_text, args=(url, return_dict, ))
		p.start()
		ans = p.join(1)
		turns = 1
		while p.is_alive():
			if turns >= 10:
				print ("killing a web search")
				p.terminate()
				p.join()
				break
			time.sleep(1)
			turns += 1
			text = return_dict['text']
		return text
	except Exception as e:
		print(e)
		return url


def pages_search(urls):
	if len(urls) < 1: return {}
	url_to_page_dictionary = {}
	for _url in urls:
		if _url not in url_to_page_dictionary:
			text = page_search(_url)
			url_to_page_dictionary[_url] = text
	return url_to_page_dictionary