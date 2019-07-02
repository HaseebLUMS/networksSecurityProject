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


trans = [
	['Welcome', 'ASUS', 'ASUS | ROUTER'],
	['Welcome', 'ZTE', 'ZTE | ROUTER'],
	['Mikro', 'MIKROTIK | ROUTER']
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


df.to_pickle('RULES')
