import os

comm1 = "python ./../local_dependency_finder.py test1.json "

testFiles = ['test1.txt', 'test2.txt', 'test3.txt', 'test4.txt', 'test5.txt', 'test6.txt', 'test7.txt', 'test8.txt', 'test9.txt', 'test10.txt']

for tf in testFiles:
	comm = comm1 + tf
	print("For ", tf, " : ")
	os.system(comm)
	print("\n\n\n")