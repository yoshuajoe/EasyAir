import re
<<<<<<< HEAD
import string, sys
=======
import string

>>>>>>> 315f2e12635f72a0f2a7dc0b16511828fa169acc

def tupling(filename):
	lines = open(filename, "r")
	sentence = []
	lineCount = 0

	# Read line by line
	# Append it to sentence
	# tupling sentence into token and type (dictionary based)
	for line in lines:
		dict = []
		for sen in line.strip("\n").split(" "):
			tmp = sen.split("=")
			dict.append({"token":tmp[0], "type":tmp[1]})
		lineCount = lineCount+1
		sentence.append({"sentence":lineCount, "content":dict})
	return sentence

def extractState(dictios):
	states = []
	for sen in dictios:
		for cont in sen['content']:
			if cont['type'] not in states:
				states.append(cont['type'])
	return states

def countStartProb(states, dictios):
	result = []
	for st in states:
		counter = 0
		for sen in dictios:
			if sen['content'][0]['type'] == st:
				counter = counter + 1
		result.append({"state":st, "prob":(counter*1.00/len(dictios))})
	return result

def occurencesState(states, dictios):
	occurences = []
	for st in states:
		wholeoccurence = 0
		for sen in dictios:
			for ct in sen['content']:
				if ct['type'] == st:
					wholeoccurence = wholeoccurence + 1
		occurences.append({"state":st, "occurences":wholeoccurence})
	return occurences

<<<<<<< HEAD
def coocurrences(dictios, states, occurencesSt):
=======
def coocurrences(dictios, states):
>>>>>>> 315f2e12635f72a0f2a7dc0b16511828fa169acc
	stOccur = []
	result = []
	tmp = []
	# map 
	for sen in dictio:
		for a in range(0, len(sen['content'])):
			if(a < (len(sen['content'])-1)):
					stOccur.append({"state_x":sen['content'][a]['type'], "state_y":sen['content'][a+1]['type']})
	# reduce
	for di in stOccur:
		count = 0
		flag = True
		#print("DI ",di)
		if len(tmp) > 0:
			for x in tmp:
				if (di["state_x"] == x["state_x"]) and (di["state_y"] == x["state_y"]):
					#print("X ",x)
					#print("cocok")
					flag = False
					break;
		
		if flag == True:
			#print("Hitung")
			for din in stOccur:
				if di == din:
					count = count + 1
<<<<<<< HEAD
					
			for ost in occurencesSt:
				if ost["state"] == di["state_x"]:
					azt = ost["occurences"]
			
			result.append({"pair":di, "count":(count*1.00/azt)})
=======
			result.append({"pair":di, "count":count})
>>>>>>> 315f2e12635f72a0f2a7dc0b16511828fa169acc
			tmp.append(di)
	
	sementara = []
	for st in states:
		for st2 in states:
			sementara.append({"pair":{"state_x":st, "state_y":st2}, "count":0})
	
	for res in result:
		for sem in sementara:
			if (sem["pair"]["state_x"] == res["pair"]["state_x"]) and (sem["pair"]["state_y"] == res["pair"]["state_y"]):
				sementara.remove(sem)

	for sem in sementara:
		result.append(sem)
	
	return result

def bagOfWord(dictios):
	tmp = []
	for sen in dictios:
		for w in sen["content"]:
			if w["token"] not in tmp:
				tmp.append(w["token"])
	return tmp
	
def countEmission(dictios, states, occurencesStates, bows):
	result = []
	for b in bows:
		tmp = []
		for st in states:
			count = 0
			azt = 0;
			for sen in dictios:
				for d in sen["content"]:
					if b == d["token"] and st == d["type"]:
						count = count + 1
			for ost in occurencesStates:
				if ost["state"] == st:
					azt = ost["occurences"]
			tmp.append({"state":st, "prob":(count*1.00/azt)})
		result.append({"word":b, "content":tmp})
	return result

<<<<<<< HEAD
def getStartProbVal(keys, list):
	for str in list:
		if str["state"] == keys:
			return str["prob"]

def getEmitVal(obs, stat, emit):
	for ob in emit:
		if ob["word"] == obs:
			for st in ob["content"]:
				if st["state"] == stat:
					return st["prob"]

def getTransVal(statx, staty, trans):
	for tr in trans:
		if tr["pair"]["state_x"] == statx and tr["pair"]["state_y"] == staty:
			return tr["count"]
					
=======
>>>>>>> 315f2e12635f72a0f2a7dc0b16511828fa169acc
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
    
    # Initialize base cases (t == 0)
    for y in states:
<<<<<<< HEAD
        V[0][y] = getStartProbVal(y, start_p) * getEmitVal(obs[0], y, emit_p)
=======
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
>>>>>>> 315f2e12635f72a0f2a7dc0b16511828fa169acc
        path[y] = [y]
    
    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
<<<<<<< HEAD
            (prob, state) = max((V[t-1][y0] * getTransVal(y0, y, trans_p) * getEmitVal(obs[t], y, emit_p), y0) for y0 in states)
=======
            (prob, state) = max((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)
>>>>>>> 315f2e12635f72a0f2a7dc0b16511828fa169acc
            V[t][y] = prob
            newpath[y] = path[state] + [y]

        # Don't need to remember the old paths
        path = newpath
    n = 0           # if only one element is observed max is sought in the initialization values
    if len(obs) != 1:
        n = t
<<<<<<< HEAD
    #print_dptable(V)
=======
    print_dptable(V)
>>>>>>> 315f2e12635f72a0f2a7dc0b16511828fa169acc
    (prob, state) = max((V[n][y], y) for y in states)
    return (prob, path[state])

# Don't study this, it just prints a table of the steps.
def print_dptable(V):
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for y in V[0]:
        s += "%.5s: " % y
        s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
        s += "\n"
    print(s)

<<<<<<< HEAD
def triples(lso):
	tripo = []
	flagS = False
	flagV = False
	flagO = False
	flagA = False
	a = None
	b = None
	c = None
	d = None
	
	for l in lso:
		if l[0] == "PER" and flagS == False:
			a = l[1]
			flagS = True
		elif l[0] == "VERB" and flagV == False:
			b = l[1]
			flagV = True
		elif l[0] == "THINGS" and flagO == False:
			c = l[1]
			flagO = True
		elif l[0] == "LOC" and flagA == False:
			d = l[1]
			flagA = True
	tripo.append((a,b,c,d))
	return tripo


def concluder(states, sta, obs):
	concluder = []
	for sp in states:
		counter = 0
		for res in sta:
			counter = counter + 1
			if sp == res:
				concluder.append((sp, obs[counter-1]))
	return concluder

def eval(t, e):
	search = 0
	for u in e:
		if u[0]=="QMTHINGS":
			fl = triples(t)
			search = 2
			return fl[0][search]
		elif u[0]=="QMLOC":
			search = 3
			fl = triples(t)
			return fl[0][search]
		elif u[0]=="QMSUB":
			search = 0
			fl = triples(t)
			return fl[0][search]
	return "I don't know"

wordAsk = None
for sy in sys.argv:
	so = sy.split("=")
	if so[0] == "-ask":
		wordAsk = so[1]
asdf = open("ori_corp.txt", "r") 
gl = []
for hj in asdf:
	hj = hj.strip("\n")
	for ty in hj.split(" "):
		gl.append(ty)
observations = tuple(gl)
dictio = tupling("anno_corp.txt")
state = extractState(dictio)
startProb = countStartProb(state, dictio)
occurencesSt = occurencesState(state, dictio)
bow = bagOfWord(dictio)
transSt = coocurrences(dictio, state, occurencesSt)
emission = countEmission(dictio, state, occurencesSt, bow)
(probs, state_res) = viterbi(observations, state, startProb, transSt, emission)
#print(vit)
concluders = concluder(state, state_res, observations)
trip = triples(concluders)	
asked = "apa yang saya makan ?"
#w = 
#print(w)
w = tuple(wordAsk.strip("\n").split(" "))
(probss, state_ress) = viterbi(w, state, startProb, transSt, emission)
concluderAsked = concluder(state, state_ress, w)
tripAsked = triples(concluderAsked)

print(wordAsk)
print(eval(concluders, concluderAsked))		


#print(sorted(concluder, key=lambda x:x[0]))














=======
def example():
    return viterbi(observations,
                   states,
                   start_probability,
                   transition_probability,
                   emission_probability)


start_probability = {'Healthy': 0.6, 'Fever': 0.4}
 
transition_probability = {
   'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},
   'Fever' : {'Healthy': 0.4, 'Fever': 0.6}
   }
 
emission_probability = {
   'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
   'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
   }
states = ('Healthy', 'Fever')
 
observations = ("Halo", "saya", "Yoshua")

#print(example())

dictio = tupling("anno.txt")
state = extractState(dictio)
startProb = countStartProb(state, dictio)
print(startProb)
occurencesSt = occurencesState(state, dictio)
#print(occurencesState(state, dictio))
bow = bagOfWord(dictio)
#print(bow)
#print(coocurrences(dictio, state))
emission = countEmission(dictio, state, occurencesSt, bow)
>>>>>>> 315f2e12635f72a0f2a7dc0b16511828fa169acc


