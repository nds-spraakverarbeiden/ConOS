import os,re,sys,traceback
from pprint import pprint

# read B4 CoNLL from stdin, writes consolidated representation of annotations to stdout
# note that this is specific to the original B4 column structure

cols=["ID","tok","WORD","aboutness","aboutness:aboutness","alliteration","alliteration:alliteration","bibl","bibl:bibl","cat","cat:cat","clause","clause:status","comment","comment:comment","context","context:context","definiteness","definiteness:definiteness","bg","bg:foc-bg","marker","marker:foc-marker","gf","gf:gf","givenness","givenness:givenness","pos","pos:pos","position","position:position","no","no:syl_no","comm","comm:top-comm","marker","trans","trans:trans"]

# # this is the full, unmodified export
# out_cols=["ID","WORD","pos", "cat","gf","clause" ,"aboutness","alliteration","bibl","context","definiteness","bg","marker","givenness","position","no","comm","marker","trans"]

# # syntax only: unmodified
# out_cols=["ID","WORD","pos", "cat","gf","clause"]

# # syntax only: aggregate PARSE
# out_cols=["ID","WORD","POS", "PARSE"]

# full export with aggregate PARSE
out_cols=["ID","WORD","PARSE" ,"aboutness","alliteration","bibl","context","definiteness","bg","marker","givenness","position","no","comm","marker","trans"]

def consolidate(buffer, incols, outcols):
	""" if "PARSE" in outcols and not "PARSE" in incols, (try to) bootstrap it """ 

	# normalize columns labels to upper case in line with CoNLL conventions
	incols = [ c.upper() for c in incols]
	outcols= [ c.upper() for c in outcols]

	result=[]
	for row in buffer:
		result.append([])
		for x,col in enumerate(outcols):
			val=None
			atts=[c for c in incols if c.startswith(col+":") ]
			if col in incols:
				if len(atts)==0:
					val=row[incols.index(col)]
				else:
					val=row[incols.index(col)]
					val=re.sub(r"^([IOBES])(-.*)?$",r"\1",val)
					vals=[ row[incols.index(att)] for att in atts ]
					if len(vals)==1 and "_" in vals and val in ["I","E"] and len(result)>1:
						# copy last vals
						last=result[-2][x]
						if last[0:2] in ["B-","I-"]:
							vals=last[2:].split("|")
					if len(set(vals))>1 or not "_" in vals:
						val=val+"-"+"|".join(vals)
			if val==None:
				val="_"
			result[-1].append(val)
	
	if "PARSE" in outcols and not "PARSE" in incols:
	
		excerpt = consolidate(buffer,incols, ["pos", "cat","gf","clause"])
		parsed=[]
	
		# operate on the outcols !
		# note that we expect uppercase col labels
		# note that this work only as long as *the annotation is consistent*, i.e.,
		# pos spans are subspans of cat spats, cats of gf, gr of clause 
		open=0
		for row in excerpt:
			parse=""
			for anno in reversed(row):	# outer to inner
				if anno[0] in ["B","S"]:
					parse=parse+"("
					open+=1
					if len(anno)>2:
						parse=parse+str(anno[2:])+" "
			parse=parse+"*"
			for anno in row:			#  inner to outer
				if anno[0] in ["E","S"]:
					parse=parse+")"
					open-=1
			if open<0:
				sys.stderr.write("warning: parentheses mismatch at row "+str(x)+": "+",".join(row)+"\n")
				sys.stderr.flush()
				open=0

			parsed.append(parse)
		if open>0:
			sys.stderr.write("warning: non-closed parenthesis at row "+str(len(excerpt)-1)+": "+",".join(excerpt[-1])+"\n")
			sys.stderr.flush()
			while(open>0):
				parsed[-1]=parsed[-1]+")"
				open=open-1
		
		for x in range(len(result)):
			result[x]=result[x][0:outcols.index("PARSE")]+[parsed[x]]+result[x][outcols.index("PARSE")+1:]
#			pprint(result[x])
	
	return result
	
buffer=[]

print("# "+"\t".join(out_cols)+"\n")

for line in sys.stdin:
	line=line.rstrip()
	if line.startswith("#"):
		print(line)
	else:
		fields=line.split("\t")
		if len(fields)!=len(cols):
			buffer=consolidate(buffer,cols,out_cols)
			print("\n".join([ "\t".join(row) for row in buffer])+"\n")
			buffer=[]
		else:
			buffer.append(fields)

if len(buffer)>0:
	buffer=consolidate(buffer,cols,out_cols)
	print("\n".join([ "\t".join(row) for row in buffer])+"\n")
