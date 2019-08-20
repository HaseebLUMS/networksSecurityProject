import json

with open('banners.json', 'r') as f:
    data = f.read()
data = json.loads(data)

testData = []
for i in range(1500, 1800):
    if data[str(i)]['protocol'] == 'HTTP':
        continue
    else:
        testData.append(data[str(i)]['banner'])

print(len(testData))
data = testData[0:50]
print((data))