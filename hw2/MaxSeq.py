import sys
import numpy as np

def vec_vec_product(vec1, vec2):
	assert(len(vec1) == len(vec2))
	rvec = []
	for i in range(len(vec1)):
		rvec.append(vec1[i] * vec2[i])
	return rvec

def calc_max(m, e, S, T):
	sensor = [S[0][1-e], S[1][1-e]]
	prob_true = vec_vec_product([T[0][0],T[1][0]], m)
	prob_false = vec_vec_product([T[0][1],T[1][1]],m)
	arrows_vecs = [np.argmax(prob_true),np.argmax(prob_false)]
	max_vec = [max(prob_true), max(prob_false)]
	return arrows_vecs, vec_vec_product(sensor, max_vec)
	

n = int(sys.argv[1])

E = []
for i in range(n):
	E.append(int(sys.argv[i+2]))

T = [[0.7, 0.3],
	 [0.4, 0.6]]

S = [[0.9, 0.1],
	 [0.3, 0.7]]

M = [[0.5,0.5]]

arrows = []

for i in range(n):
	arrows_vecs, max_vec = calc_max(M[i], E[i], S, T)
	M.append(max_vec)
	arrows.append(arrows_vecs)

best_state = np.argmax(M[-1])
path = []

for i in range(n, 0, -1):
	path[:0] = [1 - best_state]
	best_state = arrows[i-1][best_state]

print(path)

	
