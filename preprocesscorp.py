
#Author : Alfan F. Wicaksono
#IR Lab, FASILKOM, UI

#Script for pre-processing twitter corpus

from normalizer import Normalizer
from stpremoval import StpRemoval

##################### you can modify this part ######################

corpusFile = "debatcapres_2014_sesi1.txt"
preprocessedFile = "debatcapres_2014_sesi1_processed.txt"

#####################################################################

nm = Normalizer()
sw = StpRemoval()

fin  = open(corpusFile, "r")
fout = open(preprocessedFile, "w")

for line in fin:
   line = line.strip()               #remove carriage return
   line = nm.normalize(line)         #normalization
   line = sw.removeStp(line)         #remove stop word
   fout.write(line)                  #put preprocessed tweet on the new file
   fout.write("\n")

fin.close()
fout.close()


