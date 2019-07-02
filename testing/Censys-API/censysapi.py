import censys.ipv4
import json
c = censys.ipv4.CensysIPv4(api_id="425bdc11-6c8d-4f8a-a3ee-e9b1201dd288", api_secret="LavM4jWU3aeh2Tt7OhchmYAtLnWDqA3U")

IPV4_FIELDS = ['21.ftp.banner.banner', '23.telnet.banner.banner', '80.http.get.title']

data = (c.search('((protocols: "80/http") AND protocols: "21/ftp") AND protocols: "23/telnet"', 
                             IPV4_FIELDS, max_records=1000))	

banners = {}
i = 0
for d in data:
    try:
        banners[i] = {'banner': d['21.ftp.banner.banner'], 'protocol': 'FTP'}
        i += 1
    except:
        print('no ftp')
        pass
    try:
        banners[i] = {'banner': d['23.telnet.banner.banner'], 'protocol': 'TELNET'}
        i += 1
    except:
        print('no telnet')
        pass
    try:
        banners[i] = {'banner': d['80.http.get.title'], 'protocol': 'HTTP'}
        i += 1
    except:
        print('no http')
        pass

print (banners)
banners = json.dumps(banners, indent=4)
with open('banners.json', 'w') as f: f.write(banners)