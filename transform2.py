import json

fo = open('C:/Users/bayu/Desktop/output.json', 'r')
fw = open('C:/Users/bayu/Desktop/corpus.txt', 'a')


for line in fo:
	try:
		tweet = json.loads(line)
		fw.write(tweet['text']+"\n")
	except:
		continue 