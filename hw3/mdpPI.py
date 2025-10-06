# Policy Iteration

import copy
import sys
import random

S = [[1, 1], [2, 1], [3, 1], [4, 1], [1, 2], [3, 2], [4, 2], [1, 3], [2, 3], [3, 3], [4, 3]]

def is_terminal(state):
    if state not in S:
        raise ValueError("is_terminal: state {} not in S".format(state))
    if state == [4, 3] or state == [4, 2]:
        return True
    else:
        return False

A = ['up', 'down', 'left', 'right']

def outcome(state, direction):
    if state not in S:
        raise ValueError("outcome: state {} not in S".format(state))
    if direction not in A:
        raise ValueError("outcome: direction {} not in A".format(direction))

    return_state = [0, 0]

    if ((direction == 'up'    and (state[1] == 3 or state == [2, 1])) or
        (direction == 'down'  and (state[1] == 1 or state == [2, 3])) or
        (direction == 'left'  and (state[0] == 1 or state == [3, 2])) or
        (direction == 'right' and (state[0] == 4 or state == [1, 2]))):
        return_state = state
    elif direction == 'up':
        return_state = [state[0], state[1] + 1]
    elif direction == 'down':
        return_state = [state[0], state[1] - 1]
    elif direction == 'left':
        return_state = [state[0] - 1, state[1]]
    elif direction == 'right':
        return_state = [state[0] + 1, state[1]]

    if return_state not in S:
        raise ValueError("outcome: return_state {} not in S".format(return_state))

    return return_state

def P(next_state, state, action):
    if next_state not in S:
        raise ValueError("P: next_state {} not in S".format(next_state))
    if state not in S:
        raise ValueError("P: state {} not in S".format(state))
    if action not in A:
        raise ValueError("P: action {} not in A".format(action))

    next_state_prob = 0

    if action == 'up':
        if next_state == outcome(state, 'up'):
            next_state_prob += 0.8
        if next_state == outcome(state, 'left'):
            next_state_prob += 0.1
        if next_state == outcome(state, 'right'):
            next_state_prob += 0.1

    elif action == 'down':
        if next_state == outcome(state, 'down'):
            next_state_prob += 0.8
        if next_state == outcome(state, 'left'):
            next_state_prob += 0.1
        if next_state == outcome(state, 'right'):
            next_state_prob += 0.1

    elif action == 'left':
        if next_state == outcome(state, 'left'):
            next_state_prob += 0.8
        if next_state == outcome(state, 'up'):
            next_state_prob += 0.1
        if next_state == outcome(state, 'down'):
            next_state_prob += 0.1

    elif action == 'right':
        if next_state == outcome(state, 'right'):
            next_state_prob += 0.8
        if next_state == outcome(state, 'up'):
            next_state_prob += 0.1
        if next_state == outcome(state, 'down'):
            next_state_prob += 0.1

    return next_state_prob

def R(state, action, next_state):
    if next_state not in S:
        raise ValueError("R: next_state {} not in S".format(next_state))
    if state not in S:
        raise ValueError("R: state {} not in S".format(state))
    if action not in A:
        raise ValueError("R: action {} not in A".format(action))

    if is_terminal(next_state):
        return R_terminal(next_state)
    else:
        return r

def R_terminal(state):
    if not is_terminal(state):
        raise ValueError("R_terminal: state is non-terminal")

    elif state == [4, 3]:
        return float(1)
    elif state == [4, 2]:
        return float(-1)
    else:
        return 0  

U = [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]

U_old = copy.deepcopy(U)

def get_state_val(which, state):
    return which[state[0]][state[1]]

def set_state_val(which, state, val):
    which[state[0]][state[1]] = val

def Q(state, action):
    total = 0
    for i in range(len(S)):
        if is_terminal(S[i]):
            total += P(S[i], state, action) * R(state, action, S[i])
        else:
            total += P(S[i], state, action) * (R(state, action, S[i]) + gamma * get_state_val(U_old, S[i]))

    return total

pi = [[random.choice(A) for _ in range(4)] for _ in range(5)]

pi_old = copy.deepcopy(pi)

def get_policy(which, state):
	return get_state_val(which, state)

def set_policy(which, state, val):
	set_state_val(which, state, val)

def get_policy_printable(which, state):
    if get_state_val(which, state) == 'up':
        return '  up  '
    elif get_state_val(which, state) == 'down':
        return ' down '
    elif get_state_val(which, state) == 'left':
        return ' left '
    else:
        return ' right'

if len(sys.argv) != 3:
    print("Usage: $ python3 mdpPI.py <r> <gamma>")
    sys.exit()

r = float(sys.argv[1])
gamma = float(sys.argv[2])
epsilon = 0.0000001

policy_unchanged = False
improvement_iters = 0

while not policy_unchanged:
	improvement_iters += 1

	eval_iters = 0
	while eval_iters < 10:
		eval_iters += 1
		U_old = copy.deepcopy(U)
		for i in range(len(S)):
			if not is_terminal(S[i]):
				set_state_val(U, S[i], Q(S[i], get_policy(pi, S[i])))
				
	policy_unchanged = True
	for i in range(len(S)):
		up_expect = Q(S[i], 'up')
		down_expect = Q(S[i], 'down')
		left_expect = Q(S[i], 'left')
		right_expect = Q(S[i], 'right')

		best_action = 'up'
		best_action_expect = up_expect

		if down_expect > best_action_expect:
			best_action = 'down'
			best_action_expect = down_expect

		if left_expect > best_action_expect:
			best_action = 'left'
			best_action_expect = left_expect

		if right_expect > best_action_expect:
			best_action = 'right'
			best_action_expect = right_expect

		if best_action != get_policy(pi, S[i]):
			set_policy(pi, S[i], best_action)
			policy_unchanged = False

		
print("\n\t # of iterations: " + str(improvement_iters))
print("┌─────────┬───────────────┬──────────┐")
print("│  State  │  State Value  │  Policy  │")
print("├─────────┼───────────────┼──────────┤")

for i in range(len(S)):
    if not is_terminal(S[i]):
        print("│  [{:d},{:d}]  │    {: .3f}     │  {:s}  │".format(S[i][0], S[i][1], get_state_val(U, S[i]), get_policy_printable(pi, S[i])))

print("└─────────┴───────────────┴──────────┘\n")