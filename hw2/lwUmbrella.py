import sys
import random

def sample(float):
	return int(random.random() < float)

def normalize(vector):
	rvec = []
	sum = 0
	for i in range(len(vector)):
		sum += vector[i]
	for i in range(len(vector)):
		rvec.append(vector[i] / sum)
	return rvec

def prob_last_day(E, T, S, numSamples, numSteps):
	weighted_true = 0
	weighted_false = 0
	for i in range(numSamples):
		prev_day_rain = sample(0.5)
		cur_day_rain = 0
		weight = 1
		for j in range(numSteps):
			if prev_day_rain:
				cur_day_rain = sample(T[0][0])
			else:
				cur_day_rain = sample(T[1][0])
			if cur_day_rain:
				weight *= S[1][1-E[j]]
			else:
				weight *= S[0][1-E[j]]
			prev_day_rain = cur_day_rain
		if(prev_day_rain == 0):
			weighted_false += weight
		else:
			weighted_true += weight
	return normalize([weighted_true, weighted_false])


numSamples = int(sys.argv[1])

numSteps = int(sys.argv[2])

E = []
for i in range(3, numSteps+3):
	E.append(int(sys.argv[i]))

estimates = []

T = [[0.7, 0.3],
	 [0.3, 0.7]]

S = [[0.9, 0.1],
	 [0.2, 0.8]]

for i in range(10):
	estimates.append(prob_last_day(E, T, S, numSamples, numSteps)[1])

sum = 0
for i in range(10):
	sum += estimates[i]

avg = sum/10

sum_diffs = 0
for i in range(10):
	sum_diffs += pow(avg - estimates[i], 2)

variance = sum_diffs/10

print("average: " + str(avg))
print("variance: " + str(variance))
