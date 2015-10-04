import json
import time
import random
import string
import re
import codecs
import vincent
import pandas as pd
import operator

from collections import defaultdict
from collections import Counter 
from normalizer import Normalizer
from stpremoval import StpRemoval
from nltk.tokenize import word_tokenize
from sentianal import Sentianal

class CountTweet(object):
	def __init__(self):
		self.tweetMonth = {"Jan":[],"Feb":[],"Mar":[],"Apr":[],"May":[],"Jun":[],"Jul":[],"Aug":[],"Sep":[],"Oct":[],"Nov":[], "Dec":[]}
	
	def split(self, filename):
		f = open(filename, 'r')
		for line in f:
			line = line.strip()
			tweets = json.loads(line)
			t = tweets['created_at'].split(" ")
			if(t[1] == "Jan"):
				self.tweetMonth["Jan"].append(tweets)
			elif(t[1] == "Feb"):
				self.tweetMonth["Feb"].append(tweets)
			elif(t[1] == "Mar"):
				self.tweetMonth["Mar"].append(tweets)
			elif(t[1] == "Apr"):
				self.tweetMonth["Apr"].append(tweets)
			elif(t[1] == "May"):
				self.tweetMonth["May"].append(tweets)
			elif(t[1] == "Jun"):
				self.tweetMonth["Jun"].append(tweets)
			elif(t[1] == "Jul"):
				self.tweetMonth["Jul"].append(tweets)
			elif(t[1] == "Aug"):
				self.tweetMonth["Aug"].append(tweets)
			elif(t[1] == "May"):
				self.tweetMonth["May"].append(tweets)
			elif(t[1] == "Sep"):
				self.tweetMonth["Sep"].append(tweets)
			elif(t[1] == "May"):
				self.tweetMonth["May"].append(tweets)
			elif(t[1] == "Oct"):
				self.tweetMonth["Oct"].append(tweets)
			elif(t[1] == "Nov"):
				self.tweetMonth["Nov"].append(tweets)
			elif(t[1] == "Dec"):
				self.tweetMonth["Dec"].append(tweets)
		return self.tweetMonth
	
	def wordCount(self, clean_tweets, count):
		count_all = Counter()
		for ctw in clean_tweets:
			for ct in clean_tweets[ctw]:
				terms_all = ct['text_clean'].split(" ")
				count_all.update(terms_all)
		return count_all.most_common(count)
		
	def fromTuplesToJson(self, wc):
		js = []
		for w in wc:
			js.append({"word":w[0],"weight":w[1]})
		return js
		
	def count(self, tweets):
		countM = {"Jan":0,"Feb":0,"Mar":0,"Apr":0,"May":0,"Jun":0,"Jul":0,"Aug":0,"Sep":0,"Oct":0,"Nov":0, "Dec":0}
		for tw in tweets:
			countM[tw] = len(tweets[tw]) 
		return countM

	def clean(self, tweets):
		for tw in tweets:
			count = 0
			for t in tweets[tw]:
				norm = Normalizer()
				stp = StpRemoval()
				t['text_clean'] = t['text'].encode('utf-8', errors='ignore')
				t['text_clean'] = t['text_clean'].translate(string.maketrans(string.punctuation, ' ' * len(string.punctuation)))
				text = norm.normalize(t['text_clean'])
				text = stp.removeStp(t['text_clean'])
				tweets[tw][count]['text_clean'] = text.lower()
				count = count + 1
		return tweets
	
	def countPerDay(self, tweets, month):
		enum = {"Jan":31, "Feb":28, "Mar":31, "Apr":30 , "May":31, "Jun":30, "Jul":31, "Aug":31, "Sep":30, "Oct":31, "Nov":30, "Dec":31}
		month_tweets = tweets[month]
		sor = sorted(month_tweets, key=lambda x:x['created_at'][2], reverse=False)
		lst = {1:0}
		
		for i in range(enum[month]):
			lst[i+1] = 0
		
		for i in range(enum[month]):
			for tw in tweets[month]:
				t = tw['created_at'].split(" ")
				if(int(t[2]) == (i+1)):
					lst[i+1] = lst[i+1] + 1
		return lst
	
	def avgcount(self, tweets):
		countavgM = {"Jan":0,"Feb":0,"Mar":0,"Apr":0,"May":0,"Jun":0,"Jul":0,"Aug":0,"Sep":0,"Oct":0,"Nov":0, "Dec":0}
		enum = {"Jan":31, "Feb":28, "Mar":31, "Apr":30 , "May":31, "Jun":30, "Jul":31, "Aug":31, "Sep":30, "Oct":31, "Nov":30, "Dec":31}
		for tw in tweets:
			countavgM[tw] = len(tweets[tw]) * 1.00 / enum[tw]
		return countavgM
	
	def writeFile(self, filename, json):
		f = open(filename,'w')
		f.write(json) # python will convert \n to os.linesep
		f.close()
	
	def top_mentioned(self, tweets, count):
		count_all = Counter()
		for ctw in tweets:
			for ct in tweets[ctw]:
				text = ct['text'].encode("utf-8", errors='ignore')
				terms_all = [term for term in text.split(" ") if term.startswith('@')]
				count_all.update(terms_all)
		return count_all.most_common(count)
	
	def top_hash(self, tweets, count):
		count_all = Counter()
		for ctw in tweets:
			for ct in tweets[ctw]:
				text = ct['text'].encode("utf-8", errors='ignore')
				terms_all = [term for term in text.split(" ") if term.startswith('#')]
				count_all.update(terms_all)
		return count_all.most_common(count)
	
	def coocurence(self, search_word, clean_tweets):
		com = defaultdict(lambda : defaultdict(int))
		
		# f is the file pointer to the JSON data set
		for tw in clean_tweets:
			for t in clean_tweets[tw]:
				tweet = t['text_clean']
				terms_only = [term for term in tweet.split(" ")]
 
		# Build co-occurrence matrix
		for i in range(len(terms_only)-1):            
			for j in range(i+1, len(terms_only)):
				w1, w2 = sorted([terms_only[i], terms_only[j]])                
				if w1 != w2:
					com[w1][w2] += 1
					
		com_max = []
		# For each term, look for the most common co-occurrent terms
		for t1 in com:
			t1_max_terms = max(com[t1].items(), key=operator.itemgetter(1))[:5]
			for t2 in t1_max_terms:
				com_max.append(((t1, t2), com[t1][t2]))
				# Get the most frequent co-occurrences
		terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
		
		 # pass a term as a command-line argument
		count_search = Counter()
		for tw in clean_tweets:
			for t in clean_tweets[tw]:
				tweet = t['text_clean']
				terms_only = [term for term in tweet.split(" ")]
				if search_word in terms_only:
					count_search.update(terms_only)
		buff = []
		for tup in count_search.most_common(10):
			if tup[0] != search_word:
				buff.append(tup)
		return buff
	
	def getAssocTW(self, topwords, count, depth, clean_tweets):	
		big = {"name":"flare", "children":[]}
		c = 0
		for tup in topwords:
			big["children"].append({"name":tup[0], "children":[]})
			coocur = self.coocurence(tup[0], clean_tweets)
			#print(len(coocur))
			for coo in coocur:
				big["children"][c]['children'].append({"name":coo[0], "size":coo[1]})
			c = c + 1
		dump = json.dumps(big)
		self.writeFile("flare.json", dump)
		#return coocur
		
	def top_influencer(self, tweets, count):
		count_all = Counter()
		for ctw in tweets:
			for ct in tweets[ctw]:
				screen_name = [ct['user']['screen_name'].encode("utf-8", errors='ignore')]
				count_all.update(screen_name)
		return count_all.most_common(count)
	
	def sentimentAnalysis(self, tweets, month="0"):
		if month == "0":
			enum = {"Jan":31, "Feb":28, "Mar":31, "Apr":30 , "May":31, "Jun":30, "Jul":31, "Aug":31, "Sep":30, "Oct":31, "Nov":30, "Dec":31}
			tweetMonth = {"Jan":[],"Feb":[],"Mar":[],"Apr":[],"May":[],"Jun":[],"Jul":[],"Aug":[],"Sep":[],"Oct":[],"Nov":[], "Dec":[]}
			pos = neg = neu = 0
			s = Sentianal()
			for tw in tweets:
				for t in tweets[tw]:
					count = 0
					for i in range(0, enum[tw]):
						date_temp = t['created_at'].split(" ")
						date = int(date_temp[2])
						if date == (i+1):
							sentimentScore = s.compute(t['text_clean'])     #compute sentiment score of a tweet
							if sentimentScore > 0.0:            #if positive
								tweets[tw][count]['sentiment'] = 'positive'
								pos = pos + 1                         #increment the number of positive tweets
							elif sentimentScore < 0.0:          #if negative
								tweets[tw][count]['sentiment'] = 'negative'
								neg = neg + 1                         #increment the number of negative tweets
							else:
								tweets[tw][count]['sentiment'] = 'neutral'
								neu = neu + 1
					count = count + 1			
			return (tweets, pos, neg, neu)
		else:	
			enum = {"Jan":31, "Feb":28, "Mar":31, "Apr":30 , "May":31, "Jun":30, "Jul":31, "Aug":31, "Sep":30, "Oct":31, "Nov":30, "Dec":31}
			tweetMonth = {"Jan":[],"Feb":[],"Mar":[],"Apr":[],"May":[],"Jun":[],"Jul":[],"Aug":[],"Sep":[],"Oct":[],"Nov":[], "Dec":[]}
			pos = neg = neu = 0
			s = Sentianal()
			for t in tweets[month]:
				count = 0
				for i in range(0, enum[month]):
					date_temp = t['created_at'].split(" ")
					date = int(date_temp[2])
					if date == (i+1):
						sentimentScore = s.compute(t['text_clean'])     #compute sentiment score of a tweet
						if sentimentScore > 0.0:            #if positive
							tweets[month][count]['sentiment'] = 'positive'
							pos = pos + 1                         #increment the number of positive tweets
						elif sentimentScore < 0.0:          #if negative
							tweets[month][count]['sentiment'] = 'negative'
							neg = neg + 1                         #increment the number of negative tweets
						else:
							tweets[month][count]['sentiment'] = 'neutral'
							neu = neu + 1
				count = count + 1			
			return (tweets, pos, neg, neu)
			
	def geoMap(self, tweets, month):
		# Tweets are stored in "fname"
		geo_data = {
			"type": "FeatureCollection",
			"features": []
		}
		for tweet in tweets[month]:
			if tweet['coordinates']:
				geo_json_feature = {
					"type": "Feature",
					"geometry": tweet['coordinates'],
					"properties": {
						"text": tweet['text'],
						"created_at": tweet['created_at']
					}
				}
				geo_data['features'].append(geo_json_feature)
	 
		# Save geo data
		with open('geo_data.json', 'w') as fout:
			fout.write(json.dumps(geo_data, indent=4))


try:
	while True:
		print("---- Initializing -----")
		co = CountTweet()
		asd = co.split("data/stream_pilkada.json")
		print("Reading raw tweets ....")
		z = co.count(asd)
		print("Count tweets ....")
		avg = co.avgcount(asd)
		print("Count average tweets ....")
		clean = co.clean(asd)
		print("Cleanse tweets ....")
		wc = co.wordCount(clean, 50)
		print("Constructing word cloud ....")
		tmen = co.top_mentioned(asd, 10)
		print("Who mentions me ....")
		hasht = co.top_hash(asd, 5)
		print("#Hashtag ....")
		topin = co.top_influencer(asd, 10)
		print("Who's there (Influencer) ....")
		countpd = co.countPerDay(asd, "Oct")
		print("Count per day ....")
		jsonw = json.dumps(co.fromTuplesToJson(wc))
		print("Stark analyzes the tweets  ....")
		sentimen = co.sentimentAnalysis(clean)
		print("Find association ....")
		co.getAssocTW(wc,0,3, clean)
		co.writeFile("wc.json", jsonw)
		print("Loading maps ....")
		co.geoMap(asd, "Oct")
		data =  []
		labels = []
		print("Visualizing ....")
		for i in z:
			labels.append(i)
			data.append(z[i])

		data = {'data': data, 'x': labels}
		bar = vincent.Bar(data, iter_idx='x')
		bar.to_json('total_buzz.json')

		# Sentiment 
		# Total All
		data = {'positive ('+str(float(sentimen[1])/(float(sentimen[1])+float(sentimen[2])+float(sentimen[3]))*1.00*100)+' percents)': sentimen[1], 'negative ('+str(float(sentimen[2])/(float(sentimen[1])+float(sentimen[2])+float(sentimen[3]))*1.00*100)+' percents)': sentimen[2], 'neutral ('+str(float(sentimen[3])/(float(sentimen[1])+float(sentimen[2])+float(sentimen[3]))*1.00*100)+' percents)': sentimen[3]}
		pie = vincent.Pie(data)
		pie.legend('Sentiment Analysis')
		pie.to_json('sentiment_analysis.json')

		month = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov", "Dec"]
		tweetMonth = {"Jan":[],"Feb":[],"Mar":[],"Apr":[],"May":[],"Jun":[],"Jul":[],"Aug":[],"Sep":[],"Oct":[],"Nov":[], "Dec":[]}
		data = []
		for m in month:
			sen = co.sentimentAnalysis(clean, m)
			sen = {"positive":sen[1], "negative":sen[2], "neutral":sen[3]}
			data.append(sen)
			
		df = pd.DataFrame(data, index=month)
		grouped = vincent.GroupedBar(df)
		grouped.axis_titles(x='Farms', y='Produce Count')
		grouped.legend(title='Produce Types')	
		grouped.to_json("sentiment_analysis_gr.json")

		data =  []
		labels = []

		for i in tmen:
			labels.append(i[0])
			data.append(i[1])

		data = {'data': data, 'x': labels}
		bar = vincent.Bar(data, iter_idx='x')
		bar.to_json('top_mention.json')

		data =  []
		labels = []

		for i in hasht:
			labels.append(i[0])
			data.append(i[1])

		data = {'data': data, 'x': labels}
		bar = vincent.Bar(data, iter_idx='x')
		bar.to_json('top_hashtag.json')

		data =  []
		labels = []

		for i in topin:
			labels.append(i[0])
			data.append(i[1])

		data = {'data': data, 'x': labels}
		bar = vincent.Bar(data, iter_idx='x')
		bar.to_json('top_influencer.json')


		data =  []
		labels = []

		for i in avg:
			labels.append(i)
			data.append(avg[i])

		data = {'data': data, 'x': labels}
		bar = vincent.Bar(data, iter_idx='x')
		bar.to_json('avg_buzz.json')

		dates = pd.date_range(start="10/1/2015", end="10/31/2015", freq="1D")
		data = [countpd[x+1] for x in range(0,31)]
		series = pd.Series(data, index=dates)

		time_chart = vincent.Line(series)
		time_chart.axis_titles(x='Time', y='Tweets')
		time_chart.to_json('time_chart.json')
		print("It's time to sleep (10) ....")
		time.sleep(10)
except KeyboardInterrupt:
	exit()

#time_chart = vincent.Line(ITAvWAL)
#time_chart.axis_titles(x='Time', y='Freq')
#time_chart.to_json('time_chart.json')