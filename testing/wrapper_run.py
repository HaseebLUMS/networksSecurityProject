import json
import os

with open('banners.json') as b:
    data = b.read()
    data = json.loads(data)

banners = []
for i in range(0, 300):
    if (data[str(i)]['protocol'] == 'FTP') or (data[str(i)]['protocol'] == 'TELNET'):
        banners.append(data[str(i)]['banner'])

print((banners))

for i in range(0, len(banners)):
    with open('input_banner_data.txt', 'w') as f:
        f.write(banners[i])
    comm = 'python run.py'
    try:
        os.system(comm)
    except:
        pass
