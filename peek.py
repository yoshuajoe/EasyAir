
dataFile = open("debatcapres_2014_sesi1_processed.txt", "r")

for i in range(10):
   print(dataFile.readline())
dataFile.close()
