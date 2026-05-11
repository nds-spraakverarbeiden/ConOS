import sys,re,os,traceback,argparse

"""
	reading two aligned CoNLL-U files from stdin, merge annotations such that the first takes priority over the second, but the second can refine the first
	Note that we require identical tokenization and surface strings, we skip the second annotation if this is not met
"""

def update_buffer(buffer: list):
	""" buffer is list of list """
	
	result=[]
	
	try:
		result=_update_buffer(buffer)
	except:
		traceback.print_exc()
		sys.stderr.write("return first annotation only")
		result= [ row[0:10] for row in buffer ]
	
	result= [ "\t".join(row) for row in result ]
	return "\n".join(result)+"\n"

def _update_buffer(buffer:list):	
	
	# validate
	for row in buffer:
		if row[0] != row[10]:
			raise Exception("error: tokenization mismatch: "+row)
		if row[1] != row[11]:
			raise Exception("error: token mismatch: "+row)
	
	result=[]
	for row in buffer:
		misc=[]
		id=row[0]
		word=row[1]
		lemma=row[2]
		upos=row[3]
		if upos == "_":
			if row[13][0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
				upos=row[13]
		xpos=row[4]
		if row[14].startswith(xpos):
			xpos=row[14]
		feats=row[5]
		if feats=="_" and not row[15] in ["?","_",""]:
			feats=row[15]
		head=row[6]
		edge=row[7]
		if edge in ["_","dep","?"] and not row[17] in ["?","_",""]:
			edge=row[17]
			misc.append("dep<2")
			if row[16][0] in "0123456789":
				head=row[16]
				misc.append("head<2")
		
		if not head[0] in "0123456789":
			if row[16][0] in "0123456789":
				head=row[16]
				misc.append("head<2")
			else:
				misc.append("head:gap")

		if row[17].startswith(edge) and edge!=row[17]:
			edge=row[17]
			misc.append("dep<2")
		
		deps=row[8]
		if deps == "_" and row[18] not in ["_","?",""]:
			deps=row[18]
			
		if not row[19] in [ "_" , "?", "" ]:
			if len(misc)>0:
				misc=[row[19]]+misc
				# this is relevant only if any information is drawn from secondary annotation
		if not row[9] == "_":
			misc=[row[9]]+misc		
		if len(misc)==0:
			misc=["_"]
		misc="|".join(misc)
		anno=[id,word,lemma,xpos,upos,feats,head,edge,deps,misc]
		result.append(anno)
	return result
	
buffer=[]
for line in sys.stdin:
	line=line.strip()
	if line.startswith("#"):
		print(line)
	else:
		if len(line)>0 and line[0] in "0123456789":
			fields=line.split()
			if len(fields)<20:
				sys.stderr.write("warning: row "+line+" indicates an alignment error, skipping\n")
				sys.stderr.flush()
				line=""
			else:
				buffer.append(fields)
		
		if len(line)==0 and len(buffer)>0:
			print(update_buffer(buffer)+"\n")
			buffer=[]

if len(buffer)>0:
	print(update_buffer(buffer)+"\n")
			
		

