import sys,io,re,traceback

""" bootstrap Heliand-BT-style annotations from raw alignment, read from stdin """

buffer=sys.stdin.readlines()

buffer=[ row.strip() for row in buffer ]
buffer=[ row for row in buffer if len(row)>0 and not row.startswith("#") ]
buffer=[ row for row in buffer if "\t" in row ]
buffer=[ row.split("\t") for row in buffer ]

# sentence splitting
####################
last_period=0
sentence_breaks=[0]
for x,row in enumerate(buffer):
	if row[0].strip() == ".":
		last_period=x
	while(len(row)<12):
		row.append("?")
		buffer[x]=row

	# sentence breaks from alignment
	if row[2].strip() == "1" or  row[3].strip()=="1":
		# that's a bug in align.py that went unrealized because we filtered out *, before
		if not last_period+1 in sentence_breaks:
			sentence_breaks.append(last_period+1)
		elif last_period < x-5:
			sentence_breaks.append(x)
		elif row[1][0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			sentence_breaks.append(x)

	# if no alignment, then sentence break from punctuation, but only if preceeded and followed by another non-aligned row
	if row[0] == "." and "".join(sorted(set(row[3:])))=="?":
		if (x>0 and buffer[x-1][3] == "?") or (x+1<len(buffer) and (len(buffer[x+1])<4 or buffer[x+1][3] == "?")):
			sentence_breaks.append(x+1)
	# print(sentence_breaks[-1],row)

sentence_breaks.append(len(buffer))

sentences=[]
last_break=0
for s_break in sentence_breaks:
	sentences.append(buffer[last_break:s_break])
	last_break=s_break

# sentence filtering: drop gaps
###############################
for s in range(len(sentences)):
	sentence=sentences[s]
	sentence=[ row for row in sentence if not row[0][0] == "*" ]
	sentences[s]=sentence

sentences= [ sentence for sentence in sentences if len(sentence)>0 ]

#
# transform annotations
########################

# create ID, etc.
for x in range(len(sentences)):
	old=sentences[x]
	new=[]

	# old NORM WORD BT_ID BT_WORD LEMMA UPOS XPOS FEATS BT_HEAD EDGE DEPS MISC
	# new ID   WORD LEMMA UPOS XPOS FEATS BT_HEAD EDGE BT_ID MISC

	annotated=0
	bt2id={}
	last_bt=0
	consistent_ids=True
	for nr,row in enumerate(old):
		# add ID
		id=str(nr+1)
		bt_id="_"
		if consistent_ids:
			bt_id=row[2]
			if bt_id in bt2id:
				consistent_ids=False
				# print(bt_id,"in",bt2id)
				# print(row)
			elif len(bt_id)>0 and bt_id[0] in "0123456789":
				if int(bt_id)<=last_bt:
					# print(bt_id,"<=",last_bt)
					consistent_ids=False
					last_bt=int(bt_id)
					# print(row)
			if consistent_ids and bt_id[0] in "0123456789":
				bt2id[bt_id]=id

		# WORD: restore upper case
		word=row[0]
		if word[0] in "abcdefghijklmnopqrstuvwxyz":
			word = row[1][0]+word[1:]

		# POS
		upos=row[5]
		xpos=row[6]

		# I expect this to be too noisy
		lemma=row[4]
		feats="_"
		deps="_"

		bt_head=row[8]
		edge=row[9]
		misc=row[11]

		if not consistent_ids:
			# chances are high that UPOS and XPOS are ok
			lemma="_"
			feats="_"
			deps="_"
			bt_head="_"
			edge="_"
			bt_id="_"
			misc="inconsistent_id"

		if bt_head[0] in "0123456789":
			annotated+=1

		anno=[id, word, lemma, upos, xpos, feats, bt_head, edge, bt_id, misc]
		anno=[ val if val!="?" else "_" for val in anno  ]
		new.append(anno)

	# check consistency criteria
	is_consistent=True

	# requirement (1) at least 50% of all words in the sentence have an annotation
	# 				  (i.e., UPOS starting with [A-Z])
	is_consistent=annotated >= (len(new)/2)

	# requirement (2) there are no duplicate bt2id
	# these are dropped above => covered by is_consistent

	# requirement (3) bt2id are sequentially ordeed (otherwise, they come from multiple sentences)
	# also dropped above

	# drop annotations if inconsistent
	for nr in range(len(new)):
		row=new[nr]
		misc=row[9]
		if row[3]=="_":
			if misc in "_?":
				misc="no_align"
			else:
				misc="skipped"
		elif not is_consistent:
			if row[9] in "?":
				misc="no_align"
			else:
				misc="del"
			row=row[0:2]+["_"]+row[3:4]+["_"]*5+row[9:]
		elif misc in "_?":
			misc="BT"
		else:
			misc="BT"
		if row[9]!=misc:
			if row[9] in "_?":
				row[9]=misc
			else:
				row[9]+="|"+misc
		row[8]="_" # deps are abused for keeping track of btids
		new[nr]=row

	# set HEAD to new IDs
	# attach unattached PUNCT to last word
	for nr in range(len(new)):
		row=new[nr]
		if row[6] in bt2id:
			row[6]=bt2id[row[6]]
		elif not row[6]=="0": # this just stays
			if len(new)==1:
				row[6]="0"
				row[7]="root"
				row[9]="heur"
			elif row[3]=="PUNCT" and nr>1:
					row[6]=new[nr][0]
					row[7]="punct"
					row[9]="heur"
			else:
				if row[6][0:1] in "0123456789":
					row[9]=row[9]+"|dep_detached"
					row[7]="_"
				row[6]="_"
		new[nr]=row

	sentences[x]=new #+[["<="]]+old

for sentence in sentences:
	print("\n".join( [ "\t".join(row) for row in sentence ])+"\n\n")
