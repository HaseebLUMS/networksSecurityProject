from devices import devices
from vendors import vendors
from refine import refine_query as refine
from refine import refine_webpages_dictionary
from fetch_urls import perform_search as fetch_urls
from fetch_webpages import pages_search as fetch_webpages
from NER_with_local_dependencies import find_annotations
import time
web_pages_limit = 10

def ARE(banner):
	#refining the banner
	refined_banners = refine(banner, 1, devices, vendors)
	print('refined_banners', refined_banners)
	#fetching urls
	urls = []
	for _bnr in refined_banners:
		_urls = fetch_urls(_bnr)
		if len(_urls) > web_pages_limit: _urls = _urls[0:web_pages_limit]
		urls += _urls
	#fetching pages and refi
	url_to_page_dictionary = fetch_webpages(urls)
	#NER and local dependency
	annotations = find_annotations(banner, url_to_page_dictionary, devices, vendors)
	return annotations

# start = time.time()
# ARE("Welcome to RT-AC58U")
# end = time.time()
# print('Execution Time: ', end - start)