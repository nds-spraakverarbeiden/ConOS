# this is a small Python script to fix row ordering issues of CoNLLRDFFormatter -conll
# from observation, we know that every sentence is preceded by a comment, so we can assume that this is a valid marker of the beginnings of sentences
# we skip all newlines and generate them from scratch
# before comments, we insert a newline
# we order according to first field (should be ID)

import re,sys,os

id2row={}
for line in sys.stdin:
	line=line.strip()
	if(line.startswith("#")):
		if len(id2row)>0:
			print()
			for id in sorted(id2row.keys()):
				print(id2row[id])
		id2row={}
		print("\n"+line)
	elif line!="":
		fields=line.split("\t+")
		try:
			id=int(fields[0])
			id2row[id]=line			
		except:
			print("# "+line)

if len(id2row)>0:
	print()
	for id in sorted(id2row.keys()):
		print(id2row[id])
