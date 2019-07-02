
#CLASSES OF LOCAL DEPENDENCIES AS DEFINED
#IN PAPER

A = 'V.D.P'
B = '.VDP.'
C = 'VD.P'
D = 'VP.D'
E = '.VPD.'


#TEXT FROM WHICH LOCAL DEPENDENCIES ARE TO BE EXPLOITED

text = '''A mikrotik router XN-10 is a good thing.'''


#CORUPUS
setVendors = {'mikrotik', 'asus'}
setDevices = {'router', 'camera'}
setProducts = {'XN-10', 'RT-84'}


# LOGIC FOR FINDING LOCAL DEPENDENCIES
sequence = []
for ele in text.split(' '):
	if ele in setVendors:
		sequence.append({'vendor': ele})
	elif ele in setProducts:
		sequence.append({'product': ele})
	elif ele in setDevices:
		sequence.append({'device': ele})
	else:
		sequence.append({'...': ele})
ans = []
tmp = ""
for i in range(0, len(sequence)):
	if i == len(sequence)-1:
		ans.append(tmp)
	ele = sequence[i]
	if 'vendor' in ele:
		ans.append(tmp)
		tmp = ""
		if len(ans) > 0:
			tmp += '.V'
		else:
			tmp += 'V'
	elif 'product' in ele:
		tmp += 'P'
	elif 'device' in ele:
		tmp += 'D'
	else:
		if len(tmp) == 0:
			tmp += '.'
		elif not (tmp[len(tmp)-1] == '.'):
			tmp += '.'



print(ans)