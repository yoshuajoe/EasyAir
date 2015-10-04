import json
import pandas as pd
import matplotlib.pyplot as plt
import re

def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

corpus_path = 'corpus.txt'

tweets = []
corpus_file = open(corpus_path, "r")
for line in corpus_file:
    tweets.append(line)

print "Tweets count: " + str(len(tweets))

tweets_frame = pd.DataFrame()

tweets_frame['jokowi'] = map(lambda tweet: word_in_text('jokowi', tweet), tweets)
tweets_frame['prabowo'] = map(lambda tweet: word_in_text('prabowo', tweet), tweets)

print tweets_frame['jokowi'].value_counts()[True]
print tweets_frame['prabowo'].value_counts()[True]

candidates = ['jokowi', 'prabowo']
tweets_candidates = [tweets_frame['jokowi'].value_counts()[True], tweets_frame['prabowo'].value_counts()[True]]

x_pos = list(range(len(candidates)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_candidates, width, alpha=1, color='g')

# Setting axis labels and ticks
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Jokowi vs. Prabowo', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(candidates)
plt.grid()
plt.show()