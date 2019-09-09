import json

with open('TELNET.json') as f: telnet = json.loads(f.read())
with open('HTTP.json') as f: http = json.loads(f.read())
with open('ips.txt') as f: ips = f.read().split('\n')

tips = list(map(lambda x: telnet[x]['ip'], telnet))
hips = list(map(lambda x: http[x]['ip'], http))

tips = set(tips)
hips = set(hips)
ips  = set(ips )

# print(len(tips))
# print(len(hips))
# print(len( ips))

# print(len(tips.intersection(hips)))
print(len(tips.intersection(ips)))
# print(len(hips.intersection(tips)))
print(len(hips.intersection(ips)))