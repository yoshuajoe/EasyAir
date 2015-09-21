#Author : Alfan F. Wicaksono
#IR Lab, FASILKOM, UI

#Script for selecting postive/negative tweets from a corpus
#this also shows the percentage of positive vs negative tweets

from sentianal import Sentianal
import matplotlib.pyplot as plt

##################### you can modify this part ######################

corpusFile   = "jokowitweet.txt"
positiveFile = "jokowipositivetweet.txt"
negativeFile = "jokowinegativetweet.txt"

#####################################################################

s = Sentianal()

fin   = open(corpusFile, "r")
foutp = open(positiveFile, "w")
foutn = open(negativeFile, "w")

pos = 0
neg = 0

for line in fin:
   line = line.strip()
   sentimentScore = s.compute(line)     #compute sentiment score of a tweet
   if sentimentScore > 0.0:            #if positive
      pos += 1                         #increment the number of positive tweets
      foutp.write(line)                #write the positive tweet in a new file (separated)
      foutp.write("\n")
   elif sentimentScore < 0.0:          #if negative
      neg += 1                         #increment the number of negative tweets
      foutn.write(line)                #write the negative tweet in a new file (separated)
      foutn.write("\n")

fin.close()
foutp.close()
foutn.close()



###### For creating Pie Chart ########

# percentage of positve vs negative tweets

labels = 'Positive Sentiment', 'Negative Sentiment'
sizes = [float(pos)/(pos+neg), float(neg)/(pos+neg)]
colors = ['lightskyblue', 'lightcoral']
explode = (0, 0.1)

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.show()

