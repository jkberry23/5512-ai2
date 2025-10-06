import sys

def normalize(vector):
	rvec = []
	sum = 0
	for i in range(len(vector)):
		sum += vector[i]
	for i in range(len(vector)):
		rvec.append(vector[i] / sum)
	return rvec

def vec_add(vec1, vec2):
	assert(len(vec1) == len(vec2))
	rvec = []
	for i in range(len(vec1)):
		rvec.append(vec1[i] + vec2[i])
	return rvec


def vec_scalar_product(vec, n):
	rvec = []
	for i in range(len(vec)):
		rvec.append(n * vec[i])
	return rvec

def vec_vec_product(vec1, vec2):
	assert(len(vec1) == len(vec2))
	rvec = []
	for i in range(len(vec1)):
		rvec.append(vec1[i] * vec2[i])
	return rvec

def calc_forward(f, e, S, T):
	prediction = vec_add(vec_scalar_product(T[0], f[0]), 
						 vec_scalar_product(T[1], f[1]))
	update = vec_vec_product([S[0][1-e], S[1][1-e]], prediction)
	return normalize(update)

def calc_backward(b, e, S, T):
	sensor_recursion = vec_vec_product([S[0][1-e], S[1][1-e]], b)
	return vec_add(vec_scalar_product([T[0][0], T[1][0]], sensor_recursion[0]), 
				   vec_scalar_product([T[0][1], T[1][1]], sensor_recursion[1]))

n = int(sys.argv[1])

E = []
for i in range(2, n+2):
	E.append(int(sys.argv[i]))

T = [[0.7, 0.3],
	 [0.4, 0.6]]

S = [[0.9, 0.1],
	 [0.3, 0.7]]

F = [[0.5,0.5]]

smoothed = []

for i in range(n):
	F.append(calc_forward(F[i], E[i], S, T))

B = [1,1]

for i in range(n, -1, -1):
	smoothed[:0] = [normalize(vec_vec_product(B, F[i]))]
	B = calc_backward(B, E[i-1], S, T)

for i in range(1, len(smoothed)):
	print("Day {:2d} Rain Probability ([T, F]) = [{:.6f}, {:.6f}]".format(i, smoothed[i][0], smoothed[i][1]))

