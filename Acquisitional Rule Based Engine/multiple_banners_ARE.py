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
	with open('./Log_Files/ferretUniBanners.json') as f: BANNERS = json.loads(f.read())
	BANNERS = BANNERS['banners']
	print(len(BANNERS))
	BANNERS = sorted(BANNERS, key=len)
	banners = []
	for i, ele in enumerate(BANNERS):
		banners.append([ele, i])
	print(len(banners))
	banners = banners[69:]
	# process_method_on_list(ARE, banners[11:])
	for ele in banners:
		ARE(ele)


start = time.time()
main()
end = time.time()
print('Execution Time: ', end - start)
