#Author : Alfan F. Wicaksono
#IR Lab, FASILKOM, UI

#Script for selecting several tweets from corpus based on a keyword

######################### you can modify this part #############################

corpusFile = "debatcapres_2014_sesi1_processed.txt"
newFile    = "jokowitweet.txt"
keyword    = "jokowi"

################################################################################

fin  = open(corpusFile, "r")
fout = open(newFile, "w")

for line in fin:
   if keyword in line:
      fout.write(line)

fin.close()
fout.close()

