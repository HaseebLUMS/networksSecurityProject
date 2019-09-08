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
	# with open('./Log_Files/old_banners.json') as f: BANNERS = json.loads(f.read())
	# ref_banners = {}
	# for i, ele in enumerate(BANNERS):
	# 	ref = ARE([BANNERS[ele], i])
	# 	if len(ref) >= 1 and ref[0] == " ":
	# 		ref = ref[1:]
	# 	ref_banners[ele] = ref
	# with open('./Log_Files/ref_banners.json', 'w') as f: f.write(json.dumps(ref_banners, indent=4))
	ARE(['Welcome to MikroTik router MikroTik', 0])
start = time.time()
main()
end = time.time()
print('Execution Time: ', end - start)
