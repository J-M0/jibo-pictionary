import os
import re
dir = ["chair","dog","cat","sunglasses","house"]
for directory in dir:
	f = os.listdir(directory)
	for filename in f:
		file = open(directory+"/"+filename,'rb')
		l=file.readlines()
		print "Processing "+directory+"/"+filename
		if(re.findall('html', l[0], flags=re.IGNORECASE)):
			print "GOT IN"
			os.remove(directory+"/"+filename)
			print "Removing "+directory+"/"+filename
		if(len(l)>1):
			if(re.findall('html', l[1], flags=re.IGNORECASE)):
				print "GOT IN"
				os.remove(directory+"/"+filename)
				print "Removing "+directory+"/"+filename
		if(re.findall('GIF89', l[0], flags=re.I)):
			print "GOT IN"
			os.remove(directory+"/"+filename)
			print "Removing "+directory+"/"+filename





# file = open("sunglasses/165.jpg")
# l=file.readlines()
# if(re.match('html', l[0], re.IGNORECASE)):
