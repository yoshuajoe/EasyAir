from ner_clean import NER
from concluder import Concluder
from difflib import SequenceMatcher
import itertools
import re

ner = NER()
asdfgh = ner.train("anno_corp.txt")
sun = ner.recall("ori_corp.txt")

newsen = ner.loadSentence("ori_corp.txt")
bigres = []

def similar(a, b):
	return SequenceMatcher(None, a, b).ratio()

for i in range(len(newsen)):
	res = []
	for j in newsen[i].split(" "):
		for k in sun[i]:
			if j==k[1]:
				res.append((k[0], j))
				break
	bigres.append(res)

bigres2 = []
for g in bigres:
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
	bigres2.append(g)

#print(bigres2)
#entity resolution
enres = []
for bg in bigres2:
	for cbg in bg:
		if cbg[0] == "PER":
			enres.append(cbg)

memo_enres = []
for name_a in enres:
	count = 0
	for name in enres:
		count  = count + 1
		if similar(name_a[1], name[1]) >= 0.5:
			if(len(name_a[1]) >= len(name[1])):
				memo_enres.append((enres[count-1], name_a))
				enres[count-1] = name_a
			else:
				memo_enres.append((enres[count-1], name))
				enres[count-1] = name

for memo in memo_enres:
	ct = 0
	for bgr in bigres2:
		count = 0
		for bg in bgr:
			#print(memo[0])
			if bg[1] == memo[0][1]:
				#print(bigres2[ct][count][1])
				#print(memo[1])
				bigres2[ct][count] = memo[1]
			count = count +1
		ct = ct+1

str = ""
for bg in bigres2:
	for b in bg:
		str = str+b[1]+" "
	str = str[0:len(str)-1]
	str = str +". "

#print(str)
#coreference matcher
#sorry i skip this due to laziness in reading paper

#print(bigres2[7])

capture = []
stemp = []

# capture all composed sentence
for bg in bigres2:
	for b in bg:
		if b[0] == "AND":
			capture.append(bg)
			break

			
			
# process AND
for capt in capture:
	index = []
	restofword = []
	newsen = []
	lst = []
	s_and = []
	
	for rst in range(len(capt)):
		restofword.append(rst)
	
	for c in range(len(capt)):
		if capt[c][0] == "AND":
			index.append(c)
	
	for ind in index:
		s_and.append([ind-1,ind+1])
		restofword.remove(ind-1)
		restofword.remove(ind+1)
		restofword.remove(ind)
	
	res_and = []
	if len(s_and) > 1:
		for hg in range(len(s_and)-1):
			s_and[hg+1] = list(itertools.product(s_and[hg], s_and[hg+1]))
			s_and.remove(s_and[hg])
			
	for s_a in s_and:
		for sa in s_a:
			sa = list(sa)
			for rsr in restofword:
				sa.append(rsr)
			newsen.append(sa)
	#print(newsen)
	
	for d in newsen:
		newsen2bg = []
		for n in sorted(d, reverse=False):
			newsen2bg.append(capt[n])
		bigres2.append(newsen2bg)
	
	bigres2.remove(capt)
	
print(bigres2)