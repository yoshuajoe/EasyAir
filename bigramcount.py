
#Author : Alfan F. Wicaksono
#IR Lab, FASILKOM, UI

#Script for computing top-N bigram

from collections import Counter
import re

############### You can modify this part ##############

fileName = "prabowonegativetweet.txt"
topN     = 100

#######################################################

fin = open(fileName, "r")
words = re.findall('\w+', fin.read())

c = Counter(zip(words,words[1:]))
kv = c.most_common(topN)

for k,v in kv:
   print(k, v)

