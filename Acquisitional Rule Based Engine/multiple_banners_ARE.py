from are import ARE
import multiprocessing

def main():
	# BANNERS = ["MikroTik Router", "ASUS RT-AC58U", "DiskStation"]
	# pool = multiprocessing.Pool(processes=10)
	# result_list = pool.map(ARE, BANNERS)
	# print(result_list)
	ans = ARE("MikroTik Router")
	print(ans)
main()