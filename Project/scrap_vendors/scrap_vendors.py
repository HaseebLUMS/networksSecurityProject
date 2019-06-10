'''
Name: scrap_vendors.py
Argument: none
Output: A vendors.txt file with vendor names of IoT devices
How to run: python3 scrap_vendors.py
What does it do:
	--Go to https://www.iotone.com/suppliers?page=n and 
	  fetch all vendors present on page.
	--n varies from 1 to 77 as there are total 77 pages
Note:
	Uses selenium for scraping instead of fast alternatives because
	xpath changes if the request is not made through a browser. So
	by selenium, request is made through a browser and vendors are
	easily fetched
'''

from lxml import html
import requests
from selenium import webdriver


'''
Goes to "site" and fetches vendors by xpath
'''

def scrap(site):
	try:
		print(site)

		browser = webdriver.Firefox(executable_path='./geckodriver')
		browser.get(site)
		html_source = browser.page_source
		browser.close()
		tree = html.fromstring(html_source)

		path1= "/html/body/div[2]/div[2]/div[1]/div/div[2]/table/tbody/tr["
		path2= "]/td[3]/a/text()"

		vendors = []
		total_vendor_in_page = 30

		for ven in range(total_vendor_in_page+1):
			try:
				if ven is 0: continue
				path = path1+str(ven)+path2
				vendor_name = tree.xpath(path)
				for v in vendor_name: vendors.append(v.lower())
			except:
				continue
		return vendors
	except:
		return []



'''
calls scrap on each of 77 pages of site 
https://www.iotone.com/suppliers and writes
to file vendors.txt
'''
def main():
	root_site = 'https://www.iotone.com/suppliers'
	#https://www.iotone.com/suppliers?page=1
	total_pages = 77
	vendors = set()
	for page_n in range(total_pages+1):
		if page_n is 0: continue
		site = root_site + '?page=' + str(page_n)
		res = scrap(site)
		resStr = ""
		for r in res: resStr += (r+'\n')
		with open('vendors.txt', 'a+') as f: 
			f.write(resStr)
		vendors.update(res)
	print(vendors)

main()