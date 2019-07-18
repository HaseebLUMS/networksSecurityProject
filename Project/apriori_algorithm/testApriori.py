'''
Note: Prediction element is like "x | y" or "x | y | z"
	x = vendor
	y = device type
	z = product number

This file runs aprori algo and 
writes the inferred rule in file "RULES"
'''


from apyori import apriori
import json
import pandas as pd


#tells whether the length of two 
#sets is different or not
def are_diff(a, b):
	l = len(a.difference(b))
	if l:
		return 1
	else:
		return 0

'''
tells whether a set contains
prediction element 
Note: Prediction element is like "x | y" or "x | y | z"
	x = vendor
	y = device type
	z = product number
'''
def contains_prediction(a):
	if len(a) < 2:
		return False
	pred = False
	for e in a:
		if " | " in e:
			pred  = True
	return pred


'''
--Runs aprori algo
--filters the rules based
	on thresholf of support and
	confidence
--writes the inferred rule in file "RULES"
'''
def run_apriori(trans):
	results = list(apriori(trans, min_support=0.001, min_confidence=0.5) ) 

	print(len(results))
	df = pd.DataFrame(columns=('Items','Support','Confidence'))
	Support = []
	Confidence = []
	Items = []
	for RelationRecord in results:
		for ordered_stat in RelationRecord.ordered_statistics:
			
			if((len(Items) and are_diff(Items[len(Items)-1], RelationRecord.items)) or len(Items) is 0):
				if contains_prediction(RelationRecord.items):	
					Support.append(RelationRecord.support)
					Items.append(RelationRecord.items)
					Confidence.append(ordered_stat.confidence)
			
			
			elif(not are_diff(Items[len(Items)-1], RelationRecord.items)):
				if contains_prediction(RelationRecord.items):
					Support[len(Items)-1] = (RelationRecord.support)
					Items[len(Items)-1] = (RelationRecord.items)
					Confidence[len(Items)-1] = (ordered_stat.confidence)


	df['Items'] = list(map(set, Items))                                   
	df['Support'] = Support
	df['Confidence'] = Confidence
	print(df)
	df.to_pickle('RULES')

def main():
	trans = [
		["220 luna mv 50 ftp server", "mikrotik 2", "ready", "MIKROTIK | ROUTER | v6"], 
		["mikrotik v2", "38 login", "MIKROTIK | ROUTER | layer2"], 
		["220 mikrotik ftp server", "mikrotik 6", "ready", "MIKROTIK | ROUTER | rb1100ahx4"], 
		["mikrotik v6", "term", "long", "login", "MIKROTIK | ROUTER | v6"], 
		["220 axis 214 ptz network camera 4", "oct 05 2009", "ready", "MIKROTIK | ROUTER | v6"], 
		["mikrotik v5", "20 login", "MIKROTIK | ROUTER | v6"], 
		["220 mikrotik_nexuscowork ftp server", "mikrotik 6", "ready", ""], 
		["mikrotik v6", "stable", "login", "MIKROTIK | ROUTER | v6"], 
		["220 test ftp server", "mikrotik 6", "ready", "MICROSOFT | ROUTER | one100a"], 
		["mikrotik v6", "stable", "login", "MIKROTIK | ROUTER | v6"], 
		["220 nasftpd turbo station 1", "5a server", "proftpd", "CGI | ROUTER | wrt54gs"], 
		["account", " | | "], 
		["220 ftp firmware update utility", "EPSON | CAMERA"], 
		["wl driver adapter", "gpon ont wlctl", "found login", "ASUS | ROUTER"], 
		["220 ftp firmware update utility", ""], 
		["wl driver adapter", "gpon ont wlctl", "found login", "ASUS | ROUTER"], 
		["220 ftp server ready", "ARM | TV | ipv6"], 
		["login", " | | "], 
		["220 ftp firmware update utility", "ARM | BUTTON | p1"], 
		["bcm963268 broadband router login", "IFS | ROUTER | mtdblock5"], 
		["220 ftp firmware update utility", "EPSON | CAMERA"], 
		["bcm963268 broadband router login", "IFS | ROUTER | mtdblock5"], 
		["vsftpd 3", " | | "], 
		["x86_64 hm login", "kernel 3", "x86_64", "el7", "TEAM | WATCH"], 
		["220 mikrotik ftp server", "mikrotik 6", "ready", "MIKROTIK | ROUTER | rb1100ahx4"], 
		["mikrotik v6", "stable", "login", "MIKROTIK | ROUTER | v6"], 
		["220 vec_opletnia ftp server", "mikrotik 6", "ready", ""], 
		["mikrotik v6", "5 login", "MIKROTIK | ROUTER | base64"], 
		["220 haewoo1 ftp server ready", ""], 
		["mikrotik v6", "15 login", "MIKROTIK | ROUTER | base64"], 
		["220 ftp firmware update utility", ""], 
		["bcm963268 broadband router login", "IFS | ROUTER | mtdblock5"], 
		["220 ftp firmware update utility", "ARM | BUTTON | p1"], 
		["wl driver adapter", "gpon ont wlctl", "found login", "ASUS | ROUTER"], 
		["220 ftp firmware update utility", "STAR | TV"], 
		["wl driver adapter", "gpon ont wlctl", "found login", ""], 
		["220 usina ftp server", "mikrotik 6", "ready", ""], 
		["mikrotik v6", "stable", "login", "MIKROTIK | ROUTER | v6"], 
		["220 ftpu ready", "login required", "FILAMENT | SWITCH"], 
		["localhost login", "busybox", "ARM | TRACKING | u3"], 
		["220 ftp server ready", "ARM | TV | ipv6"], ["jobs", " | | "], 
		["220 mikrotik ftp server", "mikrotik 6", "ready", "MIKROTIK | ROUTER | x86"], 
		["mikrotik v6", "stable", "login", "MIKROTIK | ROUTER | v6"], 
		["220 er75i ftp server", "gnu inetutils 1", "ready", ""], 
		["irz ruh2m router console fw", "router login", "37 ruh2m", "v ufu", "master m7_1304", "16 14", "irz", "ruh2m", "welcome", "205_vk", "ASUS | ROUTER"], 
		["220 mikrotik ftp server", "mikrotik 6", "ready", "MIKROTIK | ROUTER | x86"], 
		["mikrotik v6", "stable", "login", "MIKROTIK | ROUTER | v6"], 
		["220 mikrotik ftp server", "mikrotik 6", "ready", "MIKROTIK | ROUTER | rb1100ahx4"], 
		["mikrotik v6", "23 login", "MIKROTIK | ROUTER | base64"], ["spellcastin ') [:: ffff", "220 proftpd 1", "5b server", ""], 
		["linux 9 spellcast", "debian gnu", "login", "EXACT | TV"], 
		["user number 1", "220 ---------- welcome", "---------- 220", "server port", "local time", "50 allowed", "15 minutes", "pure", "privsep", "inactivity", "ftpd", "disconnected", "TEAM | SWITCH | posts1"], 
		["root login", "TEAM | SWITCH | esp8266"], 
		["220 ftp firmware update utility", "ARM | BUTTON | p1"], 
		["bcm963268 broadband router login", "IFS | ROUTER | mtdblock5"], 
		["220 ftp print service", "network password", "v", "use", "updating", "id", "MATRIX | TRACKING"], 
		["v", "use", "updating", "id", "STAR | WATCH"]
	]
	run_apriori(trans)

main()