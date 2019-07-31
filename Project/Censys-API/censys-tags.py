import censys.ipv4
import json
c = censys.ipv4.CensysIPv4(api_id="425bdc11-6c8d-4f8a-a3ee-e9b1201dd288", api_secret="LavM4jWU3aeh2Tt7OhchmYAtLnWDqA3U")

IPV4_FIELDS = ['ip', 'metadata.description', 'metadata.device_type', 'metadata.manufacturer', 'metadata.product']

data = (c.search('((protocols: "80/http") AND protocols: "21/ftp") AND protocols: "23/telnet"', 
                             IPV4_FIELDS, max_records=1000))	

metadata = {}
i = 0
for d in data:
    metadata[d['ip']] = d

metadata = json.dumps(metadata, indent=4)
with open('metadata.json', 'w') as f: f.write(metadata)

