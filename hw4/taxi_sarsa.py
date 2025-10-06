import sys
import random
import gymnasium as gym
import pickle
import matplotlib.pyplot as plt
import numpy as np

epsilon = 0
alpha = 0
gamma = 0

if len(sys.argv) != 4:
	epsilon = 0.1
	alpha = 0.2
	gamma = 0.99
	
else:
	epsilon = float(sys.argv[1])
	alpha = float(sys.argv[2])
	gamma = float(sys.argv[3])

num_episodes = 1000

env = gym.make("Taxi-v3")
state, info = env.reset()

sarsa_q_vals = {i: {j: 0.0 for j in range(env.action_space.n)} for i in range(env.observation_space.n)}

def update_Q(state, action, next_state, next_action, reward, terminated):
	cur_Q = sarsa_q_vals[state][action]
	next_Q = 0 if terminated else sarsa_q_vals[next_state][next_action]
	sarsa_q_vals[state][action] = cur_Q + alpha * (reward + gamma * next_Q - cur_Q)

def best_action(state):
	return max(sarsa_q_vals[state], key = sarsa_q_vals[state].get)

def choose_action(state):
	if random.random() < epsilon:
		return env.action_space.sample()
	else:
		return best_action(state)

def choose_action_random(state):
	return env.action_space.sample()

sarsa_rewards = []

for episode in range(num_episodes):
	S, info = env.reset()
	A = choose_action(S)
	ep_reward = 0
	terminated = False
	truncated = False

	while not (terminated or truncated):
		S_prime, R, terminated, truncated, info = env.step(A)
		ep_reward += R
		A_prime = choose_action(S_prime)
		update_Q(S, A, S_prime, A_prime, R, terminated)
		S = S_prime
		A = A_prime

	sarsa_rewards.append(ep_reward)

random_rewards = []

for episode in range(num_episodes):
	S, info = env.reset()
	A = choose_action_random(S)
	ep_reward = 0
	terminated = False
	truncated = False

	while not (terminated or truncated):
		S_prime, R, terminated, truncated, info = env.step(A)
		ep_reward += R
		A_prime = choose_action_random(S_prime)
		S = S_prime
		A = A_prime

	random_rewards.append(ep_reward)

env.close()

sarsa_policy = {i: {best_action(i)} for i in range(500)}

with open('taxi_sarsa_output/sarsa_q_vals.pickle', 'wb') as handle:
	pickle.dump(sarsa_q_vals, handle, protocol = pickle.HIGHEST_PROTOCOL)

with open('taxi_sarsa_output/sarsa_policy.pickle', 'wb') as handle:
	pickle.dump(sarsa_policy, handle, protocol = pickle.HIGHEST_PROTOCOL)

plt.figure(figsize=(10, 6))
plt.plot(np.arange(len(sarsa_rewards)), sarsa_rewards, label='SARSA Rewards', color='blue')
plt.plot(np.arange(len(random_rewards)), random_rewards, label='Random Rewards', color='red')
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.title('Comparison of SARSA and Random Actions')
plt.legend()
plt.grid(True)
plt.savefig('taxi_sarsa_output/rewards_plot.png')