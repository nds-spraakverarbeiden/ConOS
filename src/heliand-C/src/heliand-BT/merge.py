import os,re,sys,traceback

# usecase-specific merging routine ;)
# read CoNLL from stdin
# cols: WORD LEMMA UPOS XPOS FEATS BT_ID BT_WORD BT_LEMMA BT_UPOS BT_XPOS BT_FEATS BT_HEAD EDGE DEPS

def update(buffer: list):
	""" buffer: array of arrays, CoNLL data only """

	for x in range(len(buffer)):
		buffer[x]=[str(x+1)]+buffer[x]
	
	bt2id = { row[6]: row[0] for row in buffer if row[6][0] in "0123456789" }
	
	result=[]
	for row in buffer:
		try:
			id=row[0]
			word=row[1]
			lemma=row[2]
			upos=row[3]
			xpos=row[4]
			if row[10].startswith(xpos):
				xpos=row[10]
			else:
				xpos=xpos="|_"
			feats=row[5]
			if feats=="_" and "=" in row[11]:
				feats=row[11]
			misc="_"
			head="0"
			if row[12][0] in "123456789":
				if row[12] in bt2id:
					head=bt2id[row[12]]
					misc="dep<BT"
			if row[12]=="0":
				misc="dep<BT"
			edge="_"
			if row[13][0] in "abcdefghijklmnopqrstuvwxyz":
				edge=row[13]
			deps="_"
			if row[14][0] in "0123456789":
				deps=row[14]
			
			annos=[id,word,lemma,upos,xpos,feats,head,edge,deps,misc]
			result.append(annos)
		except:
			traceback.print_exc()
			sys.stderr.write("while processing "+str(row)+"\n")
			sys.stderr.flush()
			
	result=[ "\t".join(row) for row in result ]
	return "\n".join(result)+"\n"

buffer=[]
for line in sys.stdin:
	
	line=line.strip()
	fields=line.split()
	
	if len(line)>0 and len(fields)<14 and not line.startswith("#"):
		if line[0] in "0123456789":
			sys.stderr.write("warning: incomplete row: "+line+"\n         indicates alignment of HeliPaD sentence break with Heliand-BT annotation, skipping\n")
			line=""
		else:
			sys.stderr.write("warning: incomplete row: "+line+"\n         indicates alignment of HeliPaD annotation with Heliand-BT sentence break, filling up\n")
			while(len(fields)<14):
				fields.append("?")			
		sys.stderr.flush()
	
	if line=="":
		if len(buffer)>0:
			print(update(buffer)+"\n")
			buffer=[]
	elif line.startswith("#"):
		print(line)
	else: 
		buffer.append(fields)
		
if len(buffer)>0:
	print(update(buffer)+"\n")

