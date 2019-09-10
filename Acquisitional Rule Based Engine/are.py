'''
Main File for Acquisitional Rule-based Engine
Given a banner, returns a list of annotations
'''

import time
import json
from devices import devices
from vendors import vendors
from refine  import refine_query as refine
from refine  import refine_webpages_dictionary
from fetch_urls import perform_search as fetch_urls
from fetch_webpages import pages_search as fetch_webpages
from NER_with_local_dependencies import find_annotations
web_pages_limit = 10
unique_refined_banners = set({})
banner_to_number = {}
# with open('prev_data.json') as f: prev_data = json.loads(f.read())
''' 
Provided value is a single word or not.
If single, also appends it to single_worded_banners list
which is passed as an argument (passed by reference)
'''
def is_not_single_worded(banner, single_worded_banners):
	if banner.find(" ") == -1:
		single_worded_banners.append(banner)
		return False
	return True
'''
Given devices and vendors, returns a 
list of annotations
'''
def make_annotations(devices, vendors):
	one_worded_annotations = [] + list(map(lambda x: x.upper(), devices)) + list(map(lambda x: x.upper(), vendors))
	for d in devices:
		for v in vendors:
			tmp = v + " | " + d
			one_worded_annotations.append(tmp.upper())
	return one_worded_annotations
'''
Main function for Acquisitional Rule-based Engine
-- Refines query
-- Fetches URLs
-- Fetches Web Pages
-- Runs NER and finds local dependencies
-- returns annotations 
'''
def ARE(ARGS):
	banner = ARGS[0]
	file_number = ARGS[1]
	log = {'banner': banner}
	annotations = []
	refined_banner = refine(banner, 2, devices, vendors)
	print('Started ', file_number, ' ', refined_banner)
	refined_banners = refine(banner, 1, devices, vendors)
	log['queries'] = refined_banners
	log['refined banner'] = refined_banner
	print(refined_banners)
	if refined_banner in unique_refined_banners:
		num = banner_to_number[refined_banner]
		log['num'] = num
		log = json.dumps(log, indent=4)
		with open('./Log_Files/'+str(file_number)+'.json', 'w') as f: f.write(log)
		return
	else:
		unique_refined_banners.add(refined_banner)
		banner_to_number[refined_banner] = file_number
	single_worded_banners = []
	refined_banners = list(filter(lambda x: is_not_single_worded(x, single_worded_banners), refined_banners))
	single_worded_banners_vendors = list(filter(lambda x: x in vendors, single_worded_banners))
	single_worded_banners_devices = list(filter(lambda x: x in devices, single_worded_banners))
	one_worded_annotations = make_annotations(single_worded_banners_devices, single_worded_banners_vendors)
	annotations += one_worded_annotations
	urls = []
	url_to_page_dictionary = {}
	try: 
		for _bnr in refined_banners:
			_urls = fetch_urls(_bnr)
			if len(_urls) > web_pages_limit: _urls = _urls[0:web_pages_limit]
			urls += _urls
		log['pages'] = urls
		url_to_page_dictionary = fetch_webpages(urls)
		# if (str(file_number) in prev_data):
		# 	print('url cache hit')
		# 	urls = prev_data[str(file_number)]['pages']
		# 	url_to_page_dictionary = fetch_webpages(urls)
		# else:
		# 	urls = []
		# 	url_to_page_dictionary = fetch_webpages(urls)
	except Exception as e: 
		print('Exception: ', e)
	ner_and_ld_result = find_annotations(banner, url_to_page_dictionary, devices, vendors)
	annotations += ner_and_ld_result['annotations']
	log['annotations'] = annotations
	ner_and_ld_result.pop('annotations')
	log['pipeline_numbers'] = ner_and_ld_result
	log = json.dumps(log, indent=4)
	with open('./Log_Files/'+str(file_number)+'.json', 'w') as f: f.write(log)
	print(file_number, ' completed.')
	return annotations


# b = "HTTP/1.1 400 Bad Request\r\nServer: micro_httpd\r\nCache-Control: no-cache\r\nDate: Wed, 13 Feb 2019 17:55:20 GMT\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n<HTML><HEAD><TITLE>400 Bad Request</TITLE></HEAD>\n<BODY BGCOLOR= #cc9999 ><H4>400 Bad Request</H4>\nNo request found.\n<HR>\n<ADDRESS><A HREF= http://www.acme.com/software/micro_httpd/ >micro_httpd</A></ADDRESS>\n</BODY></HTML>\n"
# ARE([b, 0])