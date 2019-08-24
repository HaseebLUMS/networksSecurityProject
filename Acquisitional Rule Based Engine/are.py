'''
Main File for Acquisitional Rule-based Engine
Given a banner, returna a list of annotations
'''
import time
from devices import devices
from vendors import vendors
from refine  import refine_query as refine
from refine  import refine_webpages_dictionary
from fetch_urls import perform_search as fetch_urls
from fetch_webpages import pages_search as fetch_webpages
from NER_with_local_dependencies import find_annotations
web_pages_limit = 10
single_worded_banners = []
''' 
Provided value is a single word or not.
If single, also appends it to single_worded_banners list
'''
def is_not_single_worded(banner):
	if banner.find(" ") == -1:
		single_worded_banners.append(banner)
		return False
	return True
'''
Given devices and vendors, returns a 
list of annotations
'''
def make_annotations(devices, vendors):
	one_worded_annotations = []
	for d in devices:
		one_worded_annotations.append(d.upper())
		for v in vendors:
			one_worded_annotations.append(v.upper())
			tmp = v + " | " + d
			one_worded_annotations.append(tmp.upper())
	return one_worded_annotations
'''
Main function for Acquisitional Rule-based Engine
-- Refines query
-- Fetches URLs
-- Fetches Web Pages
-- Runs NER and finds local dependencies
-- return annotations 
'''
def ARE(banner):
	annotations = []
	refined_banners = refine(banner, 1, devices, vendors)
	refined_banners = list(filter(is_not_single_worded, refined_banners))
	single_worded_banners_vendors = list(filter(lambda x: x in vendors, single_worded_banners))
	single_worded_banners_devices = list(filter(lambda x: x in devices, single_worded_banners))
	one_worded_annotations = make_annotations(single_worded_banners_devices, single_worded_banners_vendors)
	print(one_worded_annotations)
	print('refined_banners', refined_banners)
	urls = []
	for _bnr in refined_banners:
		_urls = fetch_urls(_bnr)
		if len(_urls) > web_pages_limit: _urls = _urls[0:web_pages_limit]
		urls += _urls
	url_to_page_dictionary = fetch_webpages(urls)
	annotations += find_annotations(banner, url_to_page_dictionary, devices, vendors)
	
	return annotations
