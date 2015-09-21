from ner_clean import NER
from concluder import Concluder

ner = NER()
asdfgh = ner.train("anno_corp.txt")
sun = ner.recall("ori_corp.txt")

newsen = ner.loadSentence("ori_corp.txt")
bigres = []
for i in range(len(newsen)):
	res = []
	for j in newsen[i].split(" "):
		for k in sun[i]:
			if j==k[1]:
				res.append((k[0], j))
	bigres.append(res)
#print(bigres)
bigres2 = []
for g in bigres:
	#lambd = lambda x,y:((x[1]+" "+y[1]),x[0]) if (x[0]==y[0]) else x
	#print(reduce(lambd, g))
	res = []
	indexer=[]
	for d in range(len(g)-1):
		if g[d][0] == g[d+1][0]:
			cat = g[d][1]+" "+g[d+1][1]
			g[d+1]=(g[d][0],cat)
			#del g[d]
			g[d] = (None,None)
			indexer.append(g[d])
	for o in indexer:
		g.remove(o)
	print(g)