def peel_spaces(data):
	try:
		if data[0] == " ": data = data[1:]
	except:
		pass
	try:
		if data[-1] == " ": data = data[0:-1]
	except:
		pass
	return data
def peel_spaces_ex(data):
	return [peel_spaces(data)]
def refine(data):
	data = list(filter(lambda x: not(x == "" or x == " "),data))
	data = list(map(peel_spaces,data))
	return data
def split_banner(banner):
	banner = banner.split(" ")
	return refine(banner)
def split_annotation(annotations):
	annotations = annotations.split(" | ")
	return refine(annotations)
def make_transactions(banner, annotations, hof):
	transactions = list(map(lambda x: hof(banner) + split_annotation(x), annotations))
	return transactions
def make_transactions_type_1(banner, annotations):
	transactions = make_transactions(banner, annotations, peel_spaces_ex)
	return transactions
def make_transactions_type_2(banner, annotations):
	transactions = make_transactions(banner, annotations, split_banner)
	return transactions
def make_simple_transactions(banner, annotations):
	transactions = list(map(lambda x: [banner, x] , annotations))
	return transactions
# print(make_transactions_type_1("it is a banner", ["A | B | C", "X | Y", "1 | 2 | 3"]))
# print(make_simple_transactions("it is a banner", ["A | B | C", "X | Y", "1 | 2 | 3"]))