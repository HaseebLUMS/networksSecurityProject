import censys.ipv4
c = censys.ipv4.CensysIPv4(api_id="425bdc11-6c8d-4f8a-a3ee-e9b1201dd288", api_secret="LavM4jWU3aeh2Tt7OhchmYAtLnWDqA3U")

# # the report method constructs a report using a query, an aggretaion field, and the 
# # number of buckets to bin
# c.report(""" "welcome to" AND tags.raw: "http" """, field="80.http.get.headers.server.raw", buckets=5)

# # the view method lets you see the full JSON for an IP address
# c.view('8.8.8.8')

# the search method lets you search the index using indexed fields, full text, and 
# combined predicates
# for result in c.search('((protocols: "80/http") AND protocols: "21/ftp") AND protocols: "23/telnet"', max_records=100):
#     print result

# you can optionally specify which fields you want to come back for search results
IPV4_FIELDS = ['21.ftp.banner.banner', '23.telnet.banner.banner']

data = (c.search('((protocols: "80/http") AND protocols: "21/ftp") AND protocols: "23/telnet"', 
                             IPV4_FIELDS, max_records=10))	

for d in data:
	print(d)	 
# print (data)