'''
Makes all combinations of an input string
A B C
=>
A
B
C
A B
A C
B C
A B C
'''


from itertools import chain, combinations


def powerset(iterable):
    s = list(iterable)
    limit = len(s)
    if len(s) > 10:
    	limit = 10
    return chain.from_iterable(combinations(s, r) for r in range(limit+1))


def generate_queries(refined_query):
	refined_query = refined_query.split(" ")
	refined_query = [x for x in refined_query if x is not "" or x is not " "]

	queries = set({})
	for i in powerset(refined_query):
	    tmp = list(i)
	    q = ""
	    if len(tmp) > 0:
		    for i in range(0, len(tmp)-1):
		    	q += (tmp[i] + ' ') 
		    q += tmp[len(tmp)-1]
	    queries.add(q)
	ans = list(queries)
	ans = ans[1:] #removing empty element

	result = set({})
	for ele in ans:
		if ele[0] == " ":
			ele = ele[1:]
		result.add(ele)

	ans = sorted(result, key=len)
	# print(ans)
	return ans


# def main():
# 	refined_query = "A B C D E F"
# 	queries = generate_queries(refined_query)
# 	print('Total: ', len(queries))
# 	for ele in queries:
# 		print(ele)

# main()