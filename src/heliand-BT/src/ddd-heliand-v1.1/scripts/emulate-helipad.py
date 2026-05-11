# read ddd-plus-helipad.conll as argument

# expect TSV with the following columns: 

# from DDD
# 0	dword (non-normalized word)
# 1	(dword, edition)
# 2	dlemma
# 3	(rhyme)
# 4	(gloss)
# 5	dclause
# 6	(chapter)
# 7	(verse)
# 8	dnorm (normalized word)
# 9	lpos (lemma POS)
# 10	dpos
# 11	(inflClassLemma)
# 12	(inflClass)
# 13	dinfl (aka "feats")
# 14	(dfile)

# from Helipad
# 15	hid
# 16	hword
# 17	hlemma
# 18	upos
# 19	hpos
# 20	(ufeats)
# 21	hhead
# 22	hdep
# 23	(hdeps)
# 24	(hmisc)


# derive mappings (most frequent case, with confidence)

# emulate helipad:
# map DDD forms to helipad forms
# map DDD POS and FEATS to helipad feats

import sys,os,re,traceback,operator

# add tupel to dictionary
def add_to_dict(list,dict):
#	print("add_to_dict(",list,dict,")")
	if len(list)==0:
		return dict
	if len(list)==1:
		if not list[0] in dict:
			dict[list[0]]=1
		else:
			dict[list[0]]+=1
		return dict
	if list[0] in dict:
		dict[list[0]]=add_to_dict(list[1:], dict[list[0]])
	else:
		dict[list[0]]=add_to_dict(list[1:], {})
#	print(dict)
	return dict

def get_transliteration(*args):
	""" extrapolate character mapping from (frequency) dictionaries """
	result={}
	for dictionary in args:
		for key in dictionary:
			vals=dictionary[key]
			if type(dictionary[key])==str:
				vals=[dictionary[key]]
			for val in vals:
				if type(val)==type(key):
					val=str(val)
					key=str(key)
					if len(val)==len(key):
						for x in range(len(key)):
							add_to_dict([key[x],val[x]],result)
	# prune result
	for k in sorted(result.keys()):
		result[k]=max(result[k].items(), key=operator.itemgetter(1))[0]
		
	return result

def transliterate(word, src2tgt, strict=False):
	""" if strict=True, throw an exception if a source character is not met """
	for x in range(len(word)):
		if not word[x] in src2tgt:
			if strict:
				raise Exception("unsupported source character \""+word[x]+"\"")
		else:
			word=word[0:x]+src2tgt[word[x]]+word[x+1:]
	return word
	
def get_max(x2y,*keys):
	if type(x2y)==dict:
		if len(keys)==0:
			raise Exception("keys list truncated")
		if not keys[0] in x2y:
			return None
		else:
			if type(x2y[keys[0]])==dict:
				if len(keys)==1:
					return max(x2y[keys[0]].items(), key=operator.itemgetter(1))[0]
				else:
					return get_max(x2y[keys[0]],*keys[1:])
			else:
				return x2y[keys[0]]
	return x2y
	
dword2hword2freq={}	# original words
dnorm2hword2freq={}	# normalized words
dlemma2hlemma2freq={}

# using DDD pos + DDD lemma pos
dpos2lpos2hpos2freq={}
dpos2lpos2upos2freq={}
dpos2lpos2feats2hpos2freq={}

# using DDD pos alone
dpos2hpos2freq={}
dpos2upos2freq={}
dpos2feats2hpos2freq={}

# using lemma pos instead
lpos2hpos2freq={}
lpos2upos2freq={}
lpos2feats2hpos2freq={}

# using lemma to recover the expected Helipad form
hlemma2hpos2hword2freq={}

for file in sys.argv[1:]:
	with open(file,"r",errors="replace") as input:
		for line in input:
			line=line.rstrip()
			if len(line)>0 and not line.startswith("#"):
				if "#" in line:
					line=re.sub(r"([^\\])#.*",r"\1",line)
				if True:
					fields=line.split("\t")
					if len(fields) > 22:
						
						dword=fields[0]
						dnorm=fields[8]
						dlemma=fields[2]
						dpos=fields[10]
						lpos=fields[9]
						feats=fields[13]
						
						hword=fields[16]
						hlemma=fields[17]
						upos=fields[18]
						hpos=fields[19]
						
						if not dword=="?" and not hword in ["?","_"]:
							dword2hword2freq=add_to_dict([dword,hword],dword2hword2freq)
							dnorm2hword2freq=add_to_dict([dnorm,hword],dnorm2hword2freq)
							dlemma2hlemma2freq=add_to_dict([dlemma,hlemma],dlemma2hlemma2freq)
							dpos2lpos2hpos2freq=add_to_dict([dpos,lpos,hpos],dpos2lpos2hpos2freq)
							dpos2lpos2upos2freq=add_to_dict([dpos,lpos,upos],dpos2lpos2upos2freq)
							dpos2lpos2feats2hpos2freq=add_to_dict([dpos,lpos,feats,hpos],dpos2lpos2feats2hpos2freq)
							dpos2hpos2freq=add_to_dict([dpos,hpos], dpos2hpos2freq)
							dpos2upos2freq=add_to_dict([dpos,upos], dpos2upos2freq)
							dpos2feats2hpos2freq=add_to_dict([dpos,feats,hpos],dpos2feats2hpos2freq)
							lpos2hpos2freq=add_to_dict([lpos,hpos],lpos2hpos2freq)
							lpos2upos2freq=add_to_dict([lpos,upos],lpos2upos2freq)
							lpos2feats2hpos2freq=add_to_dict([lpos,feats,hpos],lpos2feats2hpos2freq)
							hlemma2hpos2hword2freq=add_to_dict([hlemma,hpos,hword], hlemma2hpos2hword2freq)
							
dchar2hchar=get_transliteration(dword2hword2freq, dnorm2hword2freq, dlemma2hlemma2freq)
							
sys.stderr.write("reading and enriching DDD-CoNLL from stdin, write Heli-CoNLLU\n")
sys.stderr.flush()


id=0
for line in sys.stdin:
	line=line.rstrip()
	if len(line)==0:
		id=0
		print(line)
	if line.startswith("#"):
		print(line)
	else:
		if "#" in line:
			comment=re.sub(r".*[^\\]#","#",line)
			if len(comment)>0 and comment!=line:
				print(comment.strip())
			line=re.sub(r".*([^\\])#.*",r"\1",line).rstrip()
		fields=line.split("\t")
		if(len(fields)!=15):	# not more, because this would mean that it has been merged with Helipad, already
			print(line)
		else:
			dwords=fields[0].split()
			dnorms=fields[8].split()
			dlemmas=fields[2].split()
			dpos=fields[10]
			lpos=fields[9]
			feats=fields[13]
			dclause=fields[5]
			
			if len(dnorms)!=len(dwords):
				dnorms=["_".join(dnorms)]*len(dwords)
				
			if len(dlemmas)!=len(dwords):
				dlemmas=["_".join(dlemmas)]*len(dnorms)
			
			# print("#",line)
			for x in range(len(dwords)):
				dword=dwords[x]
				dnorm=dnorms[x]
				dlemma=dlemmas[x]
				id+=1
				
				hlemma=dlemma
				if dlemma in dlemma2hlemma2freq:
					hlemma=max(dlemma2hlemma2freq[dlemma].items(), key=operator.itemgetter(1))[0]
				else:
					hlemma=transliterate(dlemma,dchar2hchar)
					
				hpos=get_max(dpos2lpos2feats2hpos2freq, dpos,lpos,feats)
				if not hpos:
					hpos=get_max(dpos2feats2hpos2freq, dpos,feats)
				if not hpos:
					hpos=get_max(lpos2feats2hpos2freq, lpos,feats)
				if not hpos:
					hpos=get_max(dpos2lpos2hpos2freq, dpos, lpos)
				if not hpos:
					hpos=get_max(dpos2hpos2freq, dpos)
				if not hpos:
					hpos=get_max(lpos2hpos2freq, lpos)
				
				upos=get_max(dpos2lpos2upos2freq, dpos, lpos)
				if not upos:
					upos=get_max(dpos2upos2freq, dpos)
				if not upos:
					upos=get_max(lpos2upos2freq, lpos)

				hword=None
				
				comment=[]
				
				if re.match("^[^a-zA-Z]*$",dword):
					hword=dword
				elif dword in dword2hword2freq:
					hword=max(dword2hword2freq[dword].items(), key=operator.itemgetter(1))[0]
					if re.match("^[^a-zA-Z]*$",hword):
						hword=dword
					else:
						comment=["lookup form"]
				elif dnorm in dnorm2hword2freq:
					hword=max(dnorm2hword2freq[dnorm].items(), key=operator.itemgetter(1))[0]
					comment=["lookup norm"]
				elif hlemma in hlemma2hpos2hword2freq and hpos in hlemma2hpos2hword2freq[hlemma]:
					hword=max(hlemma2hpos2hword2freq[hlemma][hpos].items(), key=operator.itemgetter(1))[0]
					comment=["extrapolated from "+hlemma+"/"+hpos]
				else:
					try:
						hword=transliterate(dword,dchar2hchar,strict=True)
						comment=["transliterate form"]
					except:
						try:
							hword=transliterate(dnorm,dchar2hchar, strict=True)
							comment=["transliterate norm, strict"]
						except:
							hword=transliterate(dnorm,dchar2hchar)
							comment=["transliterate norm, non-strict"]
					
				if dword!=hword or (len(comment)>1 and comment!=["lookup form"] ):
					comment=[dword]+comment
					comment="# "+"; ".join(comment)
				else: 
					comment=""
				print(id,hword,hlemma,upos,hpos,"_","_","_","_",dclause,comment,sep="\t")
			