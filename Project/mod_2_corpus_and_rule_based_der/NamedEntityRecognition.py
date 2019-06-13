import nltk 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import os
import sys

file = sys.argv[1]

with open(file, 'r') as f: sample = f.read()



def frequentize(sample):
	example_sent = sample
	stop_words = set(stopwords.words('english')) 
	  
	word_tokens = word_tokenize(example_sent) 
	  
	filtered_sentence = [w for w in word_tokens if not w in stop_words] 

	filtered_sentence = [] 

	for w in word_tokens: 
	    if w not in stop_words: 
	        filtered_sentence.append(w.lower()) 

	frequency_map = {}
	for e in filtered_sentence:
	    if e not in frequency_map: frequency_map[e] = 1
	    else: frequency_map[e] += 1

	return frequency_map



def find_important_word(words, corpus):
	candidates = {}
	for w in words:
		if w not in corpus: continue
		candidates[w] = corpus[w]
	candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
	ans = []
	i = 5
	for c in candidates:
		if i:
			ans.append(c[0])
			i -= 1
	return ans


def is_white(w):
	white = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-']
	for i in w.lower():
		if i not in white:
			return False
	return True


def find_pattern(words):

	#should start from alpha
	#should end at alpha
	ans = []
	for w in words:
		if w[0].isalpha() and len(w) > 4 and len(w) < 12 and w[len(w)-1].isalpha():
			if (not w.isalpha()) and is_white(w):#and is_white(w): 
				ans.append(w)
	return ans

def main():
	frequency_table = frequentize(sample)

	vendors = open(sys.argv[2]).readlines()
	vendors = [sub[ : -1] for sub in vendors if sub[len(sub)-1] is '\n'] 


	device_types = open(sys.argv[3]).readlines()
	device_types = [sub[ : -1] for sub in device_types if sub[len(sub)-1] is '\n'] 


	vendors = find_important_word(vendors, frequency_table)
	device_types = find_important_word(device_types, frequency_table)

	print('Vendor: ', vendors[0])
	print('Device: ', device_types[0])

	products = find_pattern(frequency_table.keys())
	prediction = {'vendors': vendors, 'device_types' : device_types, 'products': products}

	import json
	with open('predictions.json', 'w') as outfile: json.dump(prediction, outfile, indent=2)


main()
