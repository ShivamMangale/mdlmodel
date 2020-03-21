import re
import os

fin = open("data.txt", "rt")
fout = open("out.txt", "wt")

for line in fin:
	fout.write(re.sub('\s+',' ',line))
	
fin.close()
fout.close()
