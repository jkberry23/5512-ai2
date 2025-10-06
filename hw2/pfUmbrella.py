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

def propagate(particles_in_last_true, particles_in_last_false, T):
	particles_in_true = 0
	particles_in_false = 0
	for i in range(particles_in_last_true):
		if sample(T[0][0]) == 1:
			particles_in_true += 1
		else:
			particles_in_false += 1
	for i in range(particles_in_last_false):
		if sample(T[1][0]) == 1:
			particles_in_true += 1
		else:
			particles_in_false += 1
	return particles_in_true, particles_in_false

def weight(e, S):
	return S[0][1-e], S[1][1-e] 

def resample(particles_in_true, particles_in_false, weight_true, weight_false):
	new_particles_in_true = 0
	new_particles_in_false = 0
	for i in range(particles_in_true):
		if sample(weight_true):
			new_particles_in_true += 1
		else:
			new_particles_in_false += 1
	for i in range(particles_in_false):
		if sample(weight_false):
			new_particles_in_false += 1
		else:
			new_particles_in_true += 1
	return new_particles_in_true, new_particles_in_false

def particles_last_day(E, T, S, numSamples, numSteps):
	prob_last_day = [0.5, 0.5]
	particles_in_last_true = 0
	particles_in_last_false = 0
	particles_in_true = 0
	particles_in_false = 0
	for i in range(numSamples):
		particles_in_last_true += sample(prob_last_day[0])
	particles_in_last_false = numSamples - particles_in_last_true

	for i in range(numSteps):
		particles_in_true, particles_in_false = propagate(particles_in_last_true, particles_in_last_false, T)
		weight_true, weight_false = weight(E[i], S)
		particles_in_last_true, particles_in_last_false = resample(particles_in_true, particles_in_false, weight_true, weight_false)
	
	return normalize([particles_in_last_true, particles_in_last_false])


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
	estimates.append(particles_last_day(E, T, S, numSamples, numSteps)[1])

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