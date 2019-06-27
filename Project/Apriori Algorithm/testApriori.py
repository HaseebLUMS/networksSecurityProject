'''
Note: Prediction element is like "x | y" or "x | y | z"
'''


from apyori import apriori
import json
import pandas as pd


def are_diff(a, b):
	l = len(a.difference(b))
	if l:
		return 1
	else:
		return 0


def containsPrediction(a):
	if len(a) < 2:
		return False
	pred = False
	for e in a:
		if " | " in e:
			pred  = True
	return pred


# trans = [
# 	['Welcome', 'ASUS', 'ASUS | ROUTER'],
# 	['Welcome', 'ZTE', 'ZTE | ROUTER'],
# 	['Mikro', 'MIKROTIK | ROUTER']
# ]
# 
trans = [
[
        "mikrotik",
        "ftp",
        "server",
        "mikrotik",
        "ready",
        "MIKROTIK | ROUTER | swl5"
],

[
        "nasftpd",
        "turbo",
        "station",
        "5a",
        "server",
        "proftpd",
        "MICROSOFT | CAMERA | gene6"
    ],
[
        "bcm963268",
        "broadband",
        "router",
        "r",
        "nlogin",
        "IFS | ROUTER | mtdblock5"
    ],
[
        "mirpur",
        "ftp",
        "server",
        "mikrotik",
        "bproperty",
        "ready",
        "MIKROTIK | ROUTER | rb2011"
],

[
        "technicolor",
        "gateway",
        "login",
        "TECHNICOLOR | ROUTER | tg582n"
    ],

[
        "n66u",
        "ftp",
        "service",
        "asus",
        "rt",
        "welcome",
        "ASUS | ROUTER | n66u"
    ],

[
        "matrix",
        "setu",
        "vfxth",
        "ftp",
        "service",
        "welcome",
        "MATRIX | ROUTER"
    ],
[
        "phytoverse",
        "ftp",
        "server",
        "mikrotik",
        "ready",
        "MIKROTIK | ROUTER | rb2011"
    ]

]
results = list(apriori(trans, min_support=0.1, min_confidence=0.5) ) 

print(len(results))
df = pd.DataFrame(columns=('Items','Support','Confidence'))
Support = []
Confidence = []
Items = []
for RelationRecord in results:
	for ordered_stat in RelationRecord.ordered_statistics:
		
		if((len(Items) and are_diff(Items[len(Items)-1], RelationRecord.items)) or len(Items) is 0):
			if containsPrediction(RelationRecord.items):	
				Support.append(RelationRecord.support)
				Items.append(RelationRecord.items)
				Confidence.append(ordered_stat.confidence)
		
		
		elif(not are_diff(Items[len(Items)-1], RelationRecord.items)):
			if containsPrediction(RelationRecord.items):
				Support[len(Items)-1] = (RelationRecord.support)
				Items[len(Items)-1] = (RelationRecord.items)
				Confidence[len(Items)-1] = (ordered_stat.confidence)


df['Items'] = list(map(set, Items))                                   
df['Support'] = Support
df['Confidence'] = Confidence
print(df)
# df = removeDuplicates(df)
# print(df['Items'][0])