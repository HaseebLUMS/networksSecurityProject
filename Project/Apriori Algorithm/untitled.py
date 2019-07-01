from apyori import apriori
import json
import pandas as pd

query = ['Welcome', 'ZTE']

score = 0
df = pd.read_pickle('RULES')
data = df['Items']

max_support = 0
max_confidence = 0
ans = {}

for data_set_index in range(0, len(data)):
	for q in query:
		if q in data[data_set_index]:
			if df['Support'][data_set_index] > max_support:
				max_support = df['Support'][data_set_index]
				max_confidence = df['Confidence'][data_set_index]
				ans = df['Items'][data_set_index]


print(max_confidence, max_support, ans)
print(df)