from are import ARE
import time
import json
from multiprocessing.pool import ThreadPool


# def process_method_on_list(method_to_run, items):
# 	all_items = []
# 	pool = ThreadPool(processes = 1)
# 	try:
# 		all_items = pool.map(method_to_run, items)
# 	except Exception as e:
# 		print('Exception: ', e)
# 	pool.close()
# 	pool.join()
# 	all_items = filter(None, all_items)
# 	return all_items 

def main():
	with open('./Log_Files/FTP.json') as f: data = json.loads(f.read())
	BANNERS = list(map(lambda x: data[x], data))
	BANNERS = list(filter(lambda x: ('filezilla' not in x.lower()) and ('serve-u' not in x.lower()), BANNERS))
	BANNERS = BANNERS[43:]
	count = 43
	for ban in BANNERS:
		ARE([ban, count])
		count += 1
start = time.time()
main()
end = time.time()
print('Execution Time: ', end - start)
