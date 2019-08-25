from are import ARE
import time
from multiprocessing.pool import ThreadPool


def process_method_on_list(method_to_run, items):
	all_items = []
	pool = ThreadPool(processes = 10)
	try:
		all_items = pool.map(method_to_run, items)
	except Exception as e:
		print('Exception: ', e)
	pool.close()
	pool.join()
	all_items = filter(None, all_items)
	return all_items 

def main():
	BANNERS = ["MikroTik Router", "ASUS RT-AC58U Router", "DiskStation"]
	ans = list(process_method_on_list(ARE, BANNERS))
	print(len(ans[0]), len(ans[1]), len(ans[2]))


start = time.time()
main()
end = time.time()
print('Execution Time: ', end - start)
