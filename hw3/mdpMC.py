import copy
import sys
import random

if len(sys.argv) != 4:
    print("Usage: $ python3 mdpVI.py <r> <gamma> <epsilon>")
    sys.exit()

r = float(sys.argv[1])
gamma = float(sys.argv[2])
epsilon = float(sys.argv[3])

S = [[1, 1], [2, 1], [3, 1], [4, 1], [1, 2], [3, 2], [4, 2], [1, 3], [2, 3], [3, 3], [4, 3]]

def is_terminal(state):
    if state not in S:
        raise ValueError("is_terminal: state {} not in S".format(state))
    if state == [4, 3] or state == [4, 2]:
        return True
    else:
        return False

A = ['up', 'down', 'left', 'right']

def actual_direction(action):
	sample = random.random()
	if action == 'up' or action == 'down':
		if sample < 0.1:
			return 'left'
		elif sample < 0.2:
			return 'right'
		else:
			return action
	else: # action == 'left' or action == 'right'
		if sample < 0.1:
			return 'up'
		elif sample < 0.2:
			return 'down'
		else:
			return action

def outcome(state, action):
	return_state = [0,0]
	dirn = actual_direction(action)

	if dirn == 'up':
		return_state = [state[0],state[1]+1]
	elif dirn == 'down':
		return_state = [state[0],state[1]-1]
	elif dirn == 'left':
		return_state = [state[0]-1,state[1]]
	else: # dirn == 'right'
		return_state = [state[0]+1,state[1]]

	if return_state not in S:
		return_state = state

	return return_state

def reward(state):
	if state == [4,3]:
		return 1
	elif state == [4,2]:
		return -1
	else: # non-terminal state
		return r

def generate_episode():
	states = []
	actions = []
	rewards = [None]

	state = [4,1]

	while not is_terminal(state):
		action = policy(state)
		next_state = outcome(state, action)
		reward_val = reward(next_state)

		states.append(state)
		actions.append(action)
		rewards.append(reward_val)

		state = next_state

	return states, actions, rewards

def is_first_visit(s_ep, a_ep, t):
	s = s_ep[t]
	a = a_ep[t]
	for i in range(t):
		if s_ep[i] == s and a_ep[i] == a:
			return False

	return True

returns = [[{'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}, {'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}, {'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}, {'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}],
     	   [{'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}, {'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}, {'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}, {'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}],
     	   [{'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}, {'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}, {'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}, {'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}],
     	   [{'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}, {'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}, {'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}, {'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}],
     	   [{'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}, {'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}, {'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}, {'up' : [0,0], 'down' : [0,0], 'left' : [0,0], 'right' : [0,0]}]]

def get_return(state, action):
	return returns[state[0]][state[1]][action][0]

def get_return_ct(state, action):
	return returns[state[0]][state[1]][action][1]

def inc_return_ct(state, action):
	returns[state[0]][state[1]][action][1] += 1

def set_return(state, action, val):
	returns[state[0]][state[1]][action][0] = val

def update_return(state, action, new_reward):
	inc_return_ct(state, action)
	new_return = get_return(state, action) + (1./get_return_ct(state, action)) * (new_reward - get_return(state, action))
	set_return(state, action, new_return)
	
def Q(state, action):
	return get_return(state, action)

def A_star(state):
	upQ = Q(state, 'up')
	downQ = Q(state, 'down')
	leftQ = Q(state, 'left')
	rightQ = Q(state, 'right')

	maxQ = max(upQ, downQ, leftQ, rightQ)
	if upQ == maxQ: return 'up'
	elif downQ == maxQ: return 'down'
	elif leftQ == maxQ: return 'left'
	else: return 'right'

def A_star_printable(state):
	A_star_val = A_star(state)
	if A_star_val == 'up': return '  up  '
	elif A_star_val == 'down': return ' down '
	elif A_star_val == 'left': return ' left '
	else: return ' right'

def policy(state):
	sample = random.random()
	A_star_val = A_star(state)

	if sample < 1-epsilon:
		return A_star_val
	else:
		return random.choice(A)

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end="\r", update_interval=5):
    if iteration == 1:
        print()
    if iteration == 0 or iteration == total or (iteration / total) * 100 % update_interval == 0:
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        sys.stdout.write('\r%s |%s| %s%% %s%s' % (prefix, bar, percent, suffix, print_end))
        sys.stdout.flush()
        if iteration == total:
            print()

num_iterations = 0

while num_iterations < 10000000:
	num_iterations += 1
	episode_states, episode_actions, episode_rewards = generate_episode()
	G = 0

	for t in range(len(episode_states)-1, -1, -1):
		G = gamma * G + episode_rewards[t+1]
		if is_first_visit(episode_states, episode_actions, t):
			update_return(episode_states[t], episode_actions[t], G)

	print_progress_bar(num_iterations, 10000000, prefix='Progress:', suffix='Complete', length=40)


print()
print("┌─────────┬───────────────────────────────────────────────────────────┬──────────┐")
print("│  State  │                       Action Values                       │  Policy  │")
print("├─────────┼───────────────────────────────────────────────────────────┼──────────┤")

for i in range(len(S)):
	if not is_terminal(S[i]):
		print("│  [{:d},{:d}]  ".format(S[i][0], S[i][1]) +
			  "│ up: {:+07.3f}, down: {:+07.3f}, left: {:+07.3f}, right: {:+07.3f} ".format(Q(S[i], 'up'), Q(S[i], 'down'), Q(S[i], 'left'), Q(S[i], 'right'))+
			  "│  {:s}  │".format(A_star_printable(S[i])))

print("└─────────┴───────────────────────────────────────────────────────────┴──────────┘\n")