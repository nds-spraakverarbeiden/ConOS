import sys,os,re,traceback
# remove lines with empty tokens and update HEAD annotation

def update_buffer(buffer: list):
	""" buffer is list of list """
	
	result=[]
	for row in buffer:
		if not row[1][0] in "<*0123456789_":
			result.append(row)
	
	if len(result)<len(buffer):
		buffer=result
	
		for x in range(len(buffer)):
			buffer[x]=[str(x+1)]+buffer[x]
		
		bt2id = { row[1]: row[0] for row in buffer if row[1][0] in "0123456789" }
		buffer=[ [row[0]]+row[2:] for row in buffer ]
		
		result=[]
		for row in buffer:
			if row[6]!="0":
				if row[6] in bt2id:
					row[6]=bt2id[row[6]]
				elif row[6][0] in "0123456789":
					row[6]="_"
			result.append(row)
		
	result=["\t".join(row) for row in result ]
	return "\n".join(result)+"\n"

buffer=[]
for line in sys.stdin:
	line=line.strip()
	if line.startswith("#"):
		print(line)
	else:
		if len(line)>0 and line[0] in "0123456789":
			fields=line.split()
			if len(fields)<10:
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
