import os,re,sys
# convert Heliand-M txt (< w3m over html) to conll
# perform heuristic sentence splitting based on . plus upper case

def norm(token):
	token=token.strip()
	token=re.sub(r"[()\[\]]","",token)
	if token=="":
		token="_"
	return token.lower()

def word2conll(token,raw=None):
	if raw==None:
		raw=token
	token=token.strip()
	token=norm(token)
	if(len(token)>0):
		if token!="_" or raw!="_":
			if token==".":
				print(token+"\t"+raw)
			elif token.startswith("."):
				word2conll(".",raw)
				word2conll(token[1:],"_")
			elif "." in token:
				word2conll(token[0:token.index(".")], raw)
				word2conll(".","_")
				word2conll(token[token.index(".")+1:], "_")
			else:
				print(token+"\t"+raw)

comment=None
for line in sys.stdin:
	line=line.rstrip()
	if re.match(r"^[^ 0-9]",line):
		print("# "+line)
	elif line=="":
		print()
	else:
		line=line.split()
		if re.match(r"^[0-9]",line[0]):
			print("# "+line[0])
			line=line[1:]
		while(len(line)>0):
			#print("DEBUG:",line)
			if "<" in line[0] and comment==None:
				if not line[0].startswith("<"):
					print(word2conll(line[0].split("<")[0].strip()))
					line[0]="<"+" ".join(line[0].split("<")[1:])
				comment=[]
			if(comment!=None):
				if ">" in line[0]:
					comment.append(line[0].split(">")[0]+">")
					line[0]=" ".join(line[0].split(">")[1:]).strip()
					print("# "+" ".join(comment))
					comment=None				
				else:
					comment.append(line[0])
					line[0]=""
				if line[0]=="":
					line=line[1:]
			else:
				word2conll(line[0])
				line=line[1:]