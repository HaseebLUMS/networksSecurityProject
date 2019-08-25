'''
Note: Prediction element is like "x | y" or "x | y | z"
	x = vendor
	y = device type
	z = product number

This file runs aprori algo and 
writes the inferred rule in file "RULES"
'''


from apyori import apriori
import json
import pandas as pd


#tells whether the length of two 
#sets is different or not
def are_diff(a, b):
	l = len(a.difference(b))
	if l:
		return 1
	else:
		return 0

'''
tells whether a set contains
prediction element 
Note: Prediction element is like "x | y" or "x | y | z"
	x = vendor
	y = device type
	z = product number
'''
def contains_prediction(a):
	if len(a) < 2:
		return False
	pred = False
	for e in a:
		if " | " in e:
			pred  = True
	return pred


'''
--Runs aprori algo
--filters the rules based
	on thresholf of support and
	confidence
--writes the inferred rule in file "RULES"
'''
def run_apriori(trans):
	results = list(apriori(trans, min_support=0.001, min_confidence=0.5))
	#0.0001, 0.005
	#0.005
	#2721
	print(len(results))
	df = pd.DataFrame(columns=('Items','Support','Confidence'))
	Support = []
	Confidence = []
	Items = []
	for RelationRecord in results:
		for ordered_stat in RelationRecord.ordered_statistics:
			
			# if((len(Items) and are_diff(Items[len(Items)-1], RelationRecord.items)) or len(Items) is 0):
			# if contains_prediction(RelationRecord.items):	
			Support.append(RelationRecord.support)
			Items.append(RelationRecord.items)
			Confidence.append(ordered_stat.confidence)

			# elif(not are_diff(Items[len(Items)-1], RelationRecord.items)):
			# 	if contains_prediction(RelationRecord.items):
			# 		Support[len(Items)-1] = (RelationRecord.support)
			# 		Items[len(Items)-1] = (RelationRecord.items)
			# 		Confidence[len(Items)-1] = (ordered_stat.confidence)


	df['Items'] = list(map(set, Items))                                   
	df['Support'] = Support
	df['Confidence'] = Confidence
	df.to_csv('Rules1.csv')
	df.to_pickle('RULES')
	print(len(df['Items']))
	print(df)

def main():
	with open('type_1.json') as f: data = f.read()
	data = json.loads(data)
	trans = []

	for ele in data:
		try:
			trans += data[ele]['transactions']
		except:
			pass
	print(len(trans))
	t = json.dumps({"transactions":trans}, indent=4)
	with open("trans_rule_2.json", 'w') as f: f.write(t)
	run_apriori(trans)

main()
