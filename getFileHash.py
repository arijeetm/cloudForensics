#!/bin/pyhton

file1 = open('../testhashes/tempFile.txt', 'r')
outputFile = open('../testhashes/ComputedHashes.txt','w')
for line1 in file1:
	if "#" not in line1 and "%" not in line1:   
		MD5hash = line1.split(",") 
		print MD5hash[1], MD5hash[3].strip()
		outputFile.write("%s,%s\n" %(MD5hash[1],MD5hash[3]))
file1.close()


