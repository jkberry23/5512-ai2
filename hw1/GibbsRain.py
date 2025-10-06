import random
import sys

cloudy = random.random() < 0.5
sprinkler = True
if cloudy:
	rain = random.random() < 0.8
else:
	rain = random.random() < 0.2
wetgrass = True

if(len(sys.argv) >= 2):
	numsteps = int(sys.argv[1])
else:
	numsteps = int(input("Enter the number of steps to take: "))

count = 0

for i in range(numsteps):
	samplenum = random.random()
	if random.random() < 0.5:
		#sample cloudy
		if rain:
			cloudy = samplenum < 0.444
		else:
			cloudy = samplenum < 0.048
	
	else:
		#sample rain
		if cloudy:
			rain = samplenum < 0.815
		else:
			rain = samplenum < 0.216

	if rain:
		count += 1

print("P(r|s,w) = " + str(count) + "/" + str(numsteps) + ", or " + str(count / numsteps))