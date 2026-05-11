# remove indices and empty tokens from conll annotations
# also drop sentences with multiple roots

# stdin to stdout
import sys,re,os

from pprint import pprint

# checks validity (all heads defined, contains data, at least one head)
def is_valid(sentence):
	if len(sentence)==0:
		print("# len = 0")
		return False
	heads=set([ row[6] for row in sentence ])
	if not 0 in heads:
		print("# no head in ",heads)
		return False
	ids=set([ row[0] for row in sentence ])
	if heads-ids==set([0]):
		return True
	else:
		print("# undefined heads: "+", ".join([str(h) for h in sorted(heads-ids)]))
		return False	

# true if one root and no crossing edges
def is_projective(sentence):
	if len(sentence)==0:
		return True
		
	heads=[ row[6] for row in sentence if row[6]==0 ]
	if len(heads)!=1:
		return False
		# multiple heads or a cycle
		
	for x in range(len(sentence)-1):
		X=sentence[x][0]
		Xh=sentence[x][6]
		for y in range(x+1,len(sentence)):
			Y=sentence[y][0]
			Yh=sentence[y][6]
			if 	(Xh < Yh and Yh < X) or \
				(Yh < X and Y < Xh) or \
				(X <= Yh and Yh < Xh and Xh <= Y) or \
				(Y < Xh and Xh < Yh):
				return False

	return True
	
# expect cols 1 and 6 to be integers
# drop empty tokens
# attach all punctuation (often not projective) to the highest preceding word that is accessible
# set root label to "root"
def simplify_sentence(sentence):
	result=[]
	id2row={}
	id2id={}	# for empty words with depenents, attach these dependents to the head, point to original id
	
	# remove empty words
	for row in sentence:
		word=row[1]
		if not "*" in word and not re.match(r"^[0-9]+$",word) and not re.match(r"^<[^>]*>$",word):
			result.append(row)
			id2row[row[0]]=len(result)-1
		id2id[row[0]]=row[6]

	# reassign dependents of empty words to their parent, using original ids
	for x in range(len(result)):
		row=result[x]
		head=row[6]
		while not head in id2row and head in id2id:
			head=id2id[head]
		row[6]=head
		result[x]=row
	
	# set original ids to new ids
	for x in range(len(result)):
		row=result[x]
		id=id2row[row[0]]+1
		head=row[6]
		if head in id2row:
			head=id2row[head]+1
		row[0]=id
		row[6]=head
		result[x]=row
		
	# fix annotations
	for x in range(len(result)):
		row=result[x]
		
		# re-attach punctuation to preceding element
		if row[7]=="punct":		
			if(x==0 and len(result)>1):
				head=result[x+1][0]
				while(head > 0 and head-1 < len(result) and result[head-1][6]>0):
					head=result[head-1][6]
			else:
				head=result[x-1][0]

			row[6]=head
			
		# set root label to "root" (required by UDpipe)
		if row[6]==0:
			row[7]="root"
		
		result[x]=row
			
	return result		

sentence=[]

lastline=""
for line in sys.stdin:
	line=line.strip()
	if line.startswith("#"):
		print(line)
	else:
		lines=[line]
		fields=line.split("\t")
		if len(fields)>0 and fields[0] == "1" and lastline!="":
			lines=["",line]
		for line in lines:
			fields=line.split("\t")
			if line=="":
				if len(sentence)>0:
					sentence = simplify_sentence(sentence)
					if not is_valid(sentence):
						print("# error: invalid\n# "+"\n# ".join( [ "\t".join( [ str(val) for val in row ] ) for row in sentence ])+"\n")
					elif not is_projective(sentence):
						print("# error: non-projective\n# "+"\n# ".join( [ "\t".join( [ str(val) for val in row ] ) for row in sentence ])+"\n")
					else: 
						print("\n".join( [ "\t".join( [ str(val) for val in row ] ) for row in sentence ] ) +"\n")
					sentence=[]
				print(line)
			else:
				try:
					id=int(fields[0])
					head=int(fields[6])
					sentence.append([id]+fields[1:6]+[head]+fields[7:])
				except:
					print(line)
			lastline=line
			
if len(sentence)>0:
	sentence = simplify_sentence(sentence)
	if not is_valid(sentence):
		print("# error: invalid\n# "+"\n# ".join( [ "\t".join( [ str(val) for val in row ] ) for row in sentence ])+"\n")
	elif not is_projective(sentence):
		print("# error: non-projective\n# "+"\n# ".join( [ "\t".join( [ str(val) for val in row ] ) for row in sentence ])+"\n")
	else: 
		print("\n".join( [ "\t".join( [ str(val) for val in row ] ) for row in sentence ] ) +"\n")