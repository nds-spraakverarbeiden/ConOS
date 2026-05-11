import re,os,sys,argparse

def split(string,pfx,open,close):
	if not string.startswith(pfx):
		string=string.lstrip()
	if not string.startswith(pfx):
		raise Exception("\""+string+"\" should start with \""+pfx+"\"")
	string=string[len(pfx):]
	if not string.startswith(open):
		string=string.lstrip()
	if not string.startswith(open):
		return string,""
	depth=1
	string=string[len(open):]
	head=open
	while(depth!=0 and len(string)>0):
		if string.startswith(open):
			depth+=1
			string=string[len(open):]
			head=head+open
		elif string.startswith(close):
			depth-=1
			string=string[len(close):]
			head=head+close
		else:
			head=head+string[0:1]
			string=string[1:]
	tail=string[len(head):]
	head=head[len(open):-len(close)]
	return head,tail
	
def get_val(input, incols, rule):
	#print("get_val(",input,incols,rule,")")
	rule=rule.strip()
	result=None
	if rule in incols:
		pos = incols.index(rule)
		if len(input)>pos:
			result= "'"+input[pos]+"'"
		else:
			result="'_'"
	elif rule.startswith("concat("):
		head,tail=split(rule,"concat","(",")")
		vals=[]
		part=[]
		for x in head.split(","):
			part.append(x)
			try:
				vals.append(get_val(input,incols,",".join(part)))
				part=[]
			except:
				pass
		if len(part)>0:
			raise Exception("malformed rule \""+head+"\"")
		vals=[ val[1:-1] for val in vals]	# strip '...'
		val="".join(vals)+tail
		result= "'"+val+"'"
	elif rule.startswith("'"):
		val = re.sub(r"^(['][^']+['])\s*$",r"\1",rule)
		if val.startswith("'") and val.endswith("'"):
			result=val
		else:
			raise Exception("malformed expression: \""+rule+"\"")
	elif rule.startswith("("):	
		head,tail=split(rule,"","(",")")
		test=head.split("?")[0]
		rule_true=head.split("?")[1].split(":")[0]
		rule_false=head.split("?")[1].split(":")[1]

		cond1=get_val(input,incols, test.split("==")[0])
		cond2=get_val(input,incols, test.split("==")[1])
		if cond1==cond2:
			result=get_val(input,incols,rule_true)
		else:
			result=get_val(input,incols,rule_false)
	else:
		raise Exception("malformed rule \""+rule+"\"")
	
	#print("get_val(",input,incols,rule,")=",result)
	return result

args=argparse.ArgumentParser("row-level transformation of TSV formats: select/merge operations of cell values within a row, stdin > stdout, empty lines and lines starting with # are ignored, for empty cells/undefined values, we insert _")
args.add_argument("-in","--incols",nargs="+",action="extend", type=str, help="input columns, list of labels")
args.add_argument("-out","--outcols",nargs="+", action="extend", type=str, help="definitions for output columns, space-separated: LABEL (from incols) => its value; (LABELx=LABELy?LABELa:LABELb) => C-style conditional; concat(LABEL1,LABEL2,...) => concat vals, e.g., (ID==MID?MXPOS:concat(HPOS,DPOS))")

args=args.parse_args()

for line in sys.stdin:
	line=line.rstrip()
	if line.startswith("#") or line=="":
		print(line)
	else:
		fields=line.split("\t")
		vals=[get_val(fields,args.incols,rule) for rule in args.outcols]
		vals=[ val[1:-1] for val in vals ]	 # strip '...'
		print("\t".join(vals))


	