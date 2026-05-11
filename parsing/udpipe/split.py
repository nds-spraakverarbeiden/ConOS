# read CoNLL format from stdin and generate deterministic train, dev, test split
import sys,os,re

train=None
test=0.2
dev=0.0

argv=sys.argv

sys.stderr.write(argv[0]+" OUT_DIR [TEST [DEV [TRAIN]]]\n")
sys.stderr.flush()


try:
	tgt=argv[1]
except:
	sys.stderr.write("error: missing obligatory OUT_DIR\n")
	sys.exit()

try:
	test=float(argv[2])
	dev=float(argv[3])
	train=float(argv[4])
except:
	sys.stderr.write("warning: (optional) parameters TEST, DEV and TRAIN not fully specified, resorting to defaults\n")
	sys.stderr.flush()

	
if train==None:
	train=1.0-dev-test
	if train<=0:
		sys.stderr.write("error: parameters TEST, DEV and TRAIN should add up to 1.0\n")
		sys.exit()
		
if train+dev+test != 1.0:
	sys.stderr.write("warning: parameters TEST, DEV and TRAIN should add up to 1.0, normalizing\n")
	sys.stderr.flush()

	total=train+dev+test
	train=train/total
	dev=dev/total
	test=test/total

sys.stderr.write("running "+argv[0]+" "+tgt+" "+str(test)+" "+str(dev)+" "+str(train)+"\n")
sys.stderr.flush()

sys.stderr.write("processing CoNLL-style input from stdin\n")
sys.stderr.flush()


split=[train,dev,test]
tgts=[]
with open(os.path.join(tgt,"train.conll"), "w") as train:
	with open(os.path.join(tgt,"dev.conll"),"w") as dev:
		with open(os.path.join(tgt,"test.conll"),"w") as test:
			tgts=[train,dev,test]

			lines=[1,1,1]

			block=""
			for line in sys.stdin:
				if not line.startswith("#"):
					line=re.sub(r"([^\\])#.*",r"\1",line)
					line=line.strip()
					if len(line)==0:
						block=block.strip()
						if len(block)>0:
							total=lines[0]+lines[1]+lines[2]
							ratio=[ l/total for l in lines ]
							min=0
							for x in range(len(lines)):
								if split[x]-ratio[x]>split[min]-ratio[min]:
									min=x
							#print(ratio,min)
							lines[min]+=len(block.split("\n"))
							tgts[min].write(block+"\n\n")
							tgts[min].flush()
							block=""
					else:
						block=block+line+"\n"
			block=block.strip()
			if(len(block)>0):
				tgts[0].write(block+"\n")
				tgts[0].flush()
				
			lines=[str(l-1) for l in lines]
			sys.stderr.write("token split (TRAIN, DEV, TEST)	: "+", ".join(lines)+"\n")

					
			
