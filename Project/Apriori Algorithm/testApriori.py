from apyori import apriori

trans = [
	[['A', 'B'], ['C']],
	[['E', 'F'], ['G']],
	[['A', 'D'], ['C']],
	[['A', 'B'], ['C']],
	[['E', 'F'], ['G']],
	[['A', 'B'], ['C']],
	[['E', 'F'], ['G']],
	[['A', 'B'], ['C']],
	[['E', 'F'], ['G']],
	[['A', 'B'], ['C']],
	[['E', 'F'], ['G']],
	[['A', 'B'], ['C']],
	[['E', 'F'], ['G']],
	[['A', 'B'], ['C']],
	[['E', 'F'], ['G']],
	[['A', 'B'], ['C']],
	[['E', 'F'], ['G']]
]

results = (apriori(trans, min_confidence=0.8))

gen_obj = results

for el in gen_obj:print(el)