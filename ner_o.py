import re
import string


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

def coocurrences(dictios, states, occurencesStates):
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
					
			for ost in occurencesStates:
				if ost["state"] == di["state_x"]:
					azt = ost["occurences"]
			result.append({"pair":di, "count":(count*1.00/azt)})
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
		result.append({"word" : b, "content":tmp})
	return result

def getDicVal(dict, keyVal, keyName, val):
	for d in dict:
		if d[keyName] == keyVal:
			return d[val]
	return None
	
def viterbi(obs, states, start_p, trans_p, emit_p):
	V = [{}]
	path = {}
	# Initialize base cases (t == 0)
	i = 0
	for y in states:
		V[0][y] = getDicVal(start_p, y, "state", "prob") * emit_p[i][y][obs[0]]
		i = i + 1
        #path[y] = [y]
	#print(V)
	#print(path)

# Don't study this, it just prints a table of the steps.
def print_dptable(V):
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for y in V[0]:
        s += "%.5s: " % y
        s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
        s += "\n"
    print(s)

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
states = ('OTHER', 'LOC', 'PER')
 
observations = ("Halo", "saya", "Yoshua")

#print(example())

dictio = tupling("anno.txt")
state = extractState(dictio)
startProb = countStartProb(state, dictio)
#print(startProb)
occurencesSt = occurencesState(state, dictio)
#print(occurencesState(state, dictio))
bow = bagOfWord(dictio)
#print(bow)
#print(coocurrences(dictio, state, occurencesSt))
emission = countEmission(dictio, state, occurencesSt, bow)
#print(emission)

viterbi(observations, state, startProb, occurencesSt, emission)