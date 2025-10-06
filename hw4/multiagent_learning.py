import copy

num_games = 100

class NormalFormInit:
	def __init__(self, actions, payoffs):
		self.actions = actions
		self.payoffs = payoffs

	def get_row_payoff(self, row_action, col_action):
		return self.payoffs[row_action][col_action]['row']

	def get_col_payoff(self, row_action, col_action):
		return self.payoffs[row_action][col_action]['col']

pd_init = NormalFormInit(['Testify', 'Refuse'], {'Testify': {'Testify': {'row':1.0, 'col':1.0}, 'Refuse': {'row':5.0, 'col':0.0}},
											 	 'Refuse' : {'Testify': {'row':0.0, 'col':5.0}, 'Refuse': {'row':3.0, 'col':3.0}}})

cn_init = NormalFormInit(['Swerve', 'Straight'], {'Swerve'  : {'Swerve': {'row':3.0, 'col':3.0}, 'Straight': {'row':1.5, 'col':3.5}},
												  'Straight': {'Swerve': {'row':3.5, 'col':1.5}, 'Straight': {'row':1.0, 'col':1.0}}})

mc_init = NormalFormInit(['Action', 'Comedy'], {'Action': {'Action': {'row':3.0, 'col':2.0}, 'Comedy': {'row':0.0, 'col':0.0}},
											 	'Comedy': {'Action': {'row':0.0, 'col':0.0}, 'Comedy': {'row':2.0, 'col':3.0}}})

class T_Player:
	def __init__(self, game):
		self.game = game
		self.opp_last_move = None

	def is_row(self):
		pass

	def is_col(self):
		pass

	def get_action(self):
		if self.opp_last_move == None:
			return self.game.actions[0]
		else:
			return self.opp_last_move

	def update(self, opp_action):
		self.opp_last_move = opp_action

class F_Player:
	def __init__(self, game):
		self.game = game
		self.opp_strategy = {self.game.actions[0]: 0.5, self.game.actions[1]: 0.5}
		self.opp_actions = []
		self.which = None

	def is_row(self):
		self.which = 'row'
	
	def is_col(self):
		self.which = 'col'

	def get_action(self):
			if self.which == 'row':
				action0_payoff = (self.game.get_row_payoff(self.game.actions[0], self.game.actions[0]) * self.opp_strategy[self.game.actions[0]] +
								  self.game.get_row_payoff(self.game.actions[0], self.game.actions[0]) * self.opp_strategy[self.game.actions[1]])

				action1_payoff = (self.game.get_row_payoff(self.game.actions[1], self.game.actions[0]) * self.opp_strategy[self.game.actions[0]] +
								  self.game.get_row_payoff(self.game.actions[1], self.game.actions[1]) * self.opp_strategy[self.game.actions[1]]) 

				if action0_payoff > action1_payoff:
					return self.game.actions[0]
				else: # action0_payoff <= action1_payoff
					return self.game.actions[1]

			else: # self.which == 'col':
				action0_payoff = (self.game.get_col_payoff(self.game.actions[0], self.game.actions[0]) * self.opp_strategy[self.game.actions[0]] +
								  self.game.get_col_payoff(self.game.actions[0], self.game.actions[0]) * self.opp_strategy[self.game.actions[1]])

				action1_payoff = (self.game.get_col_payoff(self.game.actions[1], self.game.actions[0]) * self.opp_strategy[self.game.actions[0]] +
								  self.game.get_col_payoff(self.game.actions[1], self.game.actions[1]) * self.opp_strategy[self.game.actions[1]]) 

				if action0_payoff > action1_payoff:
					return self.game.actions[0]
				else: # action0_payoff <= action1_payoff
					return self.game.actions[1]

	def update(self, opp_action):
		self.opp_actions.append(opp_action)
		action0_ct = 0.0
		action1_ct = 0.0

		for i in range(len(self.opp_actions)):
			if self.opp_actions[i] == self.game.actions[0]:
				action0_ct += 1.0
			else:
				action1_ct += 1.0

		self.opp_strategy[self.game.actions[0]] = action0_ct / len(self.opp_actions)
		self.opp_strategy[self.game.actions[1]] = action1_ct / len(self.opp_actions)

class B_Player:
	def __init__(self, game):
		self.game = game
		self.which = None

	def is_row(self):
		self.which = 'row'

	def is_col(self):
		self.which = 'col'

	def get_action(self):
		if self.which == 'row':
			opp_best_action_for_action0 = None
			opp_best_action_for_action1 = None
			if (self.game.get_col_payoff(self.game.actions[0], self.game.actions[0]) > 
			    self.game.get_col_payoff(self.game.actions[0], self.game.actions[1])):
				opp_best_action_for_action0 = self.game.actions[0]
			else:
				opp_best_action_for_action0 = self.game.actions[1]

			if (self.game.get_col_payoff(self.game.actions[1], self.game.actions[0]) > 
			    self.game.get_col_payoff(self.game.actions[1], self.game.actions[1])):
				opp_best_action_for_action1 = self.game.actions[0]
			else:
				opp_best_action_for_action1 = self.game.actions[1]

			if (self.game.get_row_payoff(self.game.actions[0], opp_best_action_for_action0) >
				self.game.get_row_payoff(self.game.actions[1], opp_best_action_for_action1)):
				return self.game.actions[0]
			else:
				return self.game.actions[1]

		else: # self.which == 'col
			opp_best_action_for_action0 = None
			opp_best_action_for_action1 = None
			if (self.game.get_row_payoff(self.game.actions[0], self.game.actions[0]) > 
			    self.game.get_row_payoff(self.game.actions[1], self.game.actions[0])):
				opp_best_action_for_action0 = self.game.actions[0]
			else:
				opp_best_action_for_action0 = self.game.actions[1]

			if (self.game.get_row_payoff(self.game.actions[0], self.game.actions[1]) > 
			    self.game.get_row_payoff(self.game.actions[1], self.game.actions[1])):
				opp_best_action_for_action1 = self.game.actions[0]
			else:
				opp_best_action_for_action1 = self.game.actions[1]

			if (self.game.get_col_payoff(opp_best_action_for_action0, self.game.actions[0]) >
				self.game.get_col_payoff(opp_best_action_for_action1, self.game.actions[1])):
				return self.game.actions[0]
			else:
				return self.game.actions[1]

	def update(self, opp_action):
		pass

class G_Player:
	def __init__(self, game):
		self.game = game
		self.which = None
		self.my_move_targetable_pair = None
		self.opp_move_targetable_pair = None
		self.opp_last_move = None
		self.my_worst_move_for_opponent = None

	def is_row(self):
		self.which = 'row'

	def is_col(self):
		self.which = 'col'

	def get_action(self):
		if self.opp_move_targetable_pair == None:
			my_min_payoff = float('inf')
			opp_min_payoff = float('inf')
			if self.which == 'row':
				for i in range(len(self.game.actions)):
					for j in range(len(self.game.actions)):
						my_cur_action_payoff = self.game.get_row_payoff(self.game.actions[i],self.game.actions[j])
						if my_cur_action_payoff < my_min_payoff:
							my_min_payoff = my_cur_action_payoff
						opp_cur_action_payoff = self.game.get_col_payoff(self.game.actions[i],self.game.actions[j])
						if opp_cur_action_payoff < opp_min_payoff:
							opp_min_payoff = opp_cur_action_payoff

				for i in range(len(self.game.actions)):
					for j in range(len(self.game.actions)):
						if (self.game.get_row_payoff(self.game.actions[i],self.game.actions[j]) > my_min_payoff and
						    self.game.get_col_payoff(self.game.actions[i],self.game.actions[j]) > opp_min_payoff):
							self.opp_move_targetable_pair = self.game.actions[i]
							self.my_move_targetable_pair = self.game.actions[j]

				opp_min_forced_payoff = float('inf')
				payoff_opp_best_response_action0 = None
				if (self.game.get_col_payoff(self.game.actions[0], self.game.actions[0]) > self.game.get_col_payoff(self.game.actions[0], self.game.actions[1])):
					payoff_opp_best_response_action0 = self.game.get_col_payoff(self.game.actions[0], self.game.actions[0])
				else:
					payoff_opp_best_response_action0 = self.game.get_col_payoff(self.game.actions[0], self.game.actions[1])
				payoff_opp_best_response_action1 = None
				if(self.game.get_col_payoff(self.game.actions[1], self.game.actions[0]) > self.game.get_col_payoff(self.game.actions[1], self.game.actions[1])):
					payoff_opp_best_response_action1 = self.game.get_col_payoff(self.game.actions[1], self.game.actions[0])
				else:
					payoff_opp_best_response_action1 = self.game.get_col_payoff(self.game.actions[1], self.game.actions[1])
				if payoff_opp_best_response_action0 < payoff_opp_best_response_action1:
					self.my_worst_move_for_opponent = self.game.actions[0]
				else:
					self.my_worst_move_for_opponent = self.game.actions[1]

				
			else: # self.which == 'col'
				for i in range(len(self.game.actions)):
					for j in range(len(self.game.actions)):
						my_cur_action_payoff = self.game.get_col_payoff(self.game.actions[i],self.game.actions[j])
						if my_cur_action_payoff < my_min_payoff:
							my_min_payoff = my_cur_action_payoff
						opp_cur_action_payoff = self.game.get_row_payoff(self.game.actions[i],self.game.actions[j])
						if opp_cur_action_payoff < opp_min_payoff:
							opp_min_payoff = opp_cur_action_payoff

				for i in range(len(self.game.actions)):
					for j in range(len(self.game.actions)):
						if(self.game.get_col_payoff(self.game.actions[i],self.game.actions[j]) > my_min_payoff and
						   self.game.get_row_payoff(self.game.actions[i],self.game.actions[j]) > opp_min_payoff):
						   self.opp_move_targetable_pair = self.game.actions[i]
						   self.my_move_targetable_pair = self.game.actions[j]

				payoff_opp_best_response_action0 = None
				if(self.game.get_row_payoff(self.game.actions[0], self.game.actions[0]) > self.game.get_row_payoff(self.game.actions[1], self.game.actions[0])):
					payoff_opp_best_response_action0 = self.game.get_row_payoff(self.game.actions[0], self.game.actions[0])
				else:
					payoff_opp_best_response_action0 = self.game.get_row_payoff(self.game.actions[1], self.game.actions[0])
				payoff_opp_best_response_action1 = None
				if(self.game.get_row_payoff(self.game.actions[0],self.game.actions[1]) > self.game.get_row_payoff(self.game.actions[1],self.game.actions[1])):
					payoff_opp_best_response_action1 = self.game.get_row_payoff(self.game.actions[0], self.game.actions[1])
				else:
					payoff_opp_best_response_action1 = self.game.get_row_payoff(self.game.actions[1], self.game.actions[1])
				if payoff_opp_best_response_action0 < payoff_opp_best_response_action1:
					self.my_worst_move_for_opponent = self.game.actions[0]
				else:
					self.my_worst_move_for_opponent = self.game.actions[1]
				
		if self.opp_last_move == None or self.opp_last_move == self.opp_move_targetable_pair:
			return self.my_move_targetable_pair
		else:
			return self.my_worst_move_for_opponent

	def update(self, opp_action):
		self.opp_last_move = opp_action

class NormalFormGame:
	def __init__(self, row_player, col_player, init):
		self.row_player = row_player
		self.col_player = col_player
		self.row_player.is_row()
		self.col_player.is_col()
		self.actions = init.actions
		self.payoffs = init.payoffs
		self.row_payoff_cum = 0
		self.col_payoff_cum = 0

	def step(self):
		row_action = self.row_player.get_action()
		col_action = self.col_player.get_action()
		outcome = self.payoffs[row_action][col_action]
		self.row_payoff_cum += outcome['row']
		self.col_payoff_cum += outcome['col']
		self.row_player.update(col_action)
		self.col_player.update(row_action)

	def play(self):
		for _ in range(num_games):
			self.step()

#prisoners dilemma games
pd_tvt = NormalFormGame(T_Player(pd_init), T_Player(pd_init), pd_init)
pd_fvt = NormalFormGame(F_Player(pd_init), T_Player(pd_init), pd_init)
pd_bvt = NormalFormGame(B_Player(pd_init), T_Player(pd_init), pd_init)
pd_gvt = NormalFormGame(G_Player(pd_init), T_Player(pd_init), pd_init)

pd_fvf = NormalFormGame(F_Player(pd_init), F_Player(pd_init), pd_init)
pd_bvf = NormalFormGame(B_Player(pd_init), F_Player(pd_init), pd_init)
pd_gvf = NormalFormGame(G_Player(pd_init), F_Player(pd_init), pd_init)

pd_bvb = NormalFormGame(B_Player(pd_init), B_Player(pd_init), pd_init)
pd_gvb = NormalFormGame(G_Player(pd_init), B_Player(pd_init), pd_init)

pd_gvg = NormalFormGame(G_Player(pd_init), G_Player(pd_init), pd_init)

#chicken games
cn_tvt = NormalFormGame(T_Player(cn_init), T_Player(cn_init), cn_init)
cn_fvt = NormalFormGame(F_Player(cn_init), T_Player(cn_init), cn_init)
cn_bvt = NormalFormGame(B_Player(cn_init), T_Player(cn_init), cn_init)
cn_gvt = NormalFormGame(G_Player(cn_init), T_Player(cn_init), cn_init)

cn_fvf = NormalFormGame(F_Player(cn_init), F_Player(cn_init), cn_init)
cn_bvf = NormalFormGame(B_Player(cn_init), F_Player(cn_init), cn_init)
cn_gvf = NormalFormGame(G_Player(cn_init), F_Player(cn_init), cn_init)

cn_bvb = NormalFormGame(B_Player(cn_init), B_Player(cn_init), cn_init)
cn_gvb = NormalFormGame(G_Player(cn_init), B_Player(cn_init), cn_init)

cn_gvg = NormalFormGame(G_Player(cn_init), B_Player(cn_init), cn_init)

#movie coordination games
mc_tvt = NormalFormGame(T_Player(mc_init), T_Player(mc_init), mc_init)
mc_fvt = NormalFormGame(F_Player(mc_init), T_Player(mc_init), mc_init)
mc_bvt = NormalFormGame(B_Player(mc_init), T_Player(mc_init), mc_init)
mc_gvt = NormalFormGame(G_Player(mc_init), T_Player(mc_init), mc_init)

mc_fvf = NormalFormGame(F_Player(mc_init), F_Player(mc_init), mc_init)
mc_bvf = NormalFormGame(B_Player(mc_init), F_Player(mc_init), mc_init)
mc_gvf = NormalFormGame(G_Player(mc_init), F_Player(mc_init), mc_init)

mc_bvb = NormalFormGame(B_Player(mc_init), B_Player(mc_init), mc_init)
mc_gvb = NormalFormGame(G_Player(mc_init), B_Player(mc_init), mc_init)

mc_gvg = NormalFormGame(G_Player(mc_init), G_Player(mc_init), mc_init)


#prisoners dilemma games
pd_tvt.play()
pd_fvt.play()
pd_bvt.play()
pd_gvt.play()

pd_fvf.play()
pd_bvf.play()
pd_gvf.play()

pd_bvb.play()
pd_gvb.play()

pd_gvg.play()

#chicken games
cn_tvt.play()
cn_fvt.play()
cn_bvt.play()
cn_gvt.play()

cn_fvf.play()
cn_bvf.play()
cn_gvf.play()

cn_bvb.play()
cn_gvb.play()

cn_gvg.play()

#movie coordination games
mc_tvt.play()
mc_fvt.play()
mc_bvt.play()
mc_gvt.play()

mc_fvf.play()
mc_bvf.play()
mc_gvf.play()

mc_bvb.play()
mc_gvb.play()

mc_gvg.play()

print("\n\033[1m                               Prisoner\'s Dilemma Results                               \033[0m")
print("┌───────────────────┬───────────────┬───────────────────┬───────────────┬───────────────┐")
print("│                   │  Tit-for-tat  │  Fictitious Play  │     Bully     │   Godfather   │")
print("├───────────────────┼───────────────┼───────────────────┼───────────────┼───────────────┤")
print("│    Tit-for-tat    │ ({:.3f},{:.3f}) │                   │               │               │".format(pd_tvt.row_payoff_cum/num_games, pd_tvt.col_payoff_cum/num_games))
print("├───────────────────┼───────────────┼───────────────────┼───────────────┼───────────────┤")
print("│  Fictitious Play  │ ({:.3f},{:.3f}) │   ({:.3f},{:.3f})   │               │               │".format(pd_fvt.row_payoff_cum/num_games, pd_fvt.col_payoff_cum/num_games, pd_fvf.row_payoff_cum/num_games, pd_fvf.col_payoff_cum/num_games))
print("├───────────────────┼───────────────┼───────────────────┼───────────────┼───────────────┤")
print("│       Bully       │ ({:.3f},{:.3f}) │   ({:.3f},{:.3f})   │ ({:.3f},{:.3f}) │               │".format(pd_bvt.row_payoff_cum/num_games, pd_bvt.col_payoff_cum/num_games, pd_bvf.row_payoff_cum/num_games, pd_bvf.col_payoff_cum/num_games, pd_bvb.row_payoff_cum/num_games, pd_bvb.col_payoff_cum/num_games))
print("├───────────────────┼───────────────┼───────────────────┼───────────────┼───────────────┤")
print("│     Godfather     │ ({:.3f},{:.3f}) │   ({:.3f},{:.3f})   │ ({:.3f},{:.3f}) │ ({:.3f},{:.3f}) │".format(pd_gvt.row_payoff_cum/num_games, pd_gvt.col_payoff_cum/num_games, pd_gvf.row_payoff_cum/num_games, pd_gvf.col_payoff_cum/num_games, pd_gvb.row_payoff_cum/num_games, pd_gvb.col_payoff_cum/num_games, pd_gvg.row_payoff_cum/num_games, pd_gvg.col_payoff_cum/num_games))
print("└───────────────────┴───────────────┴───────────────────┴───────────────┴───────────────┘\n")

print("\n\033[1m                                     Chicken Results                                    \033[0m")
print("┌───────────────────┬───────────────┬───────────────────┬───────────────┬───────────────┐")
print("│                   │  Tit-for-tat  │  Fictitious Play  │     Bully     │   Godfather   │")
print("├───────────────────┼───────────────┼───────────────────┼───────────────┼───────────────┤")
print("│    Tit-for-tat    │ ({:.3f},{:.3f}) │                   │               │               │".format(cn_tvt.row_payoff_cum/num_games, cn_tvt.col_payoff_cum/num_games))
print("├───────────────────┼───────────────┼───────────────────┼───────────────┼───────────────┤")
print("│  Fictitious Play  │ ({:.3f},{:.3f}) │   ({:.3f},{:.3f})   │               │               │".format(cn_fvt.row_payoff_cum/num_games, cn_fvt.col_payoff_cum/num_games, cn_fvf.row_payoff_cum/num_games, cn_fvf.col_payoff_cum/num_games))
print("├───────────────────┼───────────────┼───────────────────┼───────────────┼───────────────┤")
print("│       Bully       │ ({:.3f},{:.3f}) │   ({:.3f},{:.3f})   │ ({:.3f},{:.3f}) │               │".format(cn_bvt.row_payoff_cum/num_games, cn_bvt.col_payoff_cum/num_games, cn_bvf.row_payoff_cum/num_games, cn_bvf.col_payoff_cum/num_games, cn_bvb.row_payoff_cum/num_games, cn_bvb.col_payoff_cum/num_games))
print("├───────────────────┼───────────────┼───────────────────┼───────────────┼───────────────┤")
print("│     Godfather     │ ({:.3f},{:.3f}) │   ({:.3f},{:.3f})   │ ({:.3f},{:.3f}) │ ({:.3f},{:.3f}) │".format(cn_gvt.row_payoff_cum/num_games, cn_gvt.col_payoff_cum/num_games, cn_gvf.row_payoff_cum/num_games, cn_gvf.col_payoff_cum/num_games, cn_gvb.row_payoff_cum/num_games, cn_gvb.col_payoff_cum/num_games, cn_gvg.row_payoff_cum/num_games, cn_gvg.col_payoff_cum/num_games))
print("└───────────────────┴───────────────┴───────────────────┴───────────────┴───────────────┘\n")

print("\n\033[1m                               Movie Coordination Results                               \033[0m")
print("┌───────────────────┬───────────────┬───────────────────┬───────────────┬───────────────┐")
print("│                   │  Tit-for-tat  │  Fictitious Play  │     Bully     │   Godfather   │")
print("├───────────────────┼───────────────┼───────────────────┼───────────────┼───────────────┤")
print("│    Tit-for-tat    │ ({:.3f},{:.3f}) │                   │               │               │".format(mc_tvt.row_payoff_cum/num_games, mc_tvt.col_payoff_cum/num_games))
print("├───────────────────┼───────────────┼───────────────────┼───────────────┼───────────────┤")
print("│  Fictitious Play  │ ({:.3f},{:.3f}) │   ({:.3f},{:.3f})   │               │               │".format(mc_fvt.row_payoff_cum/num_games, mc_fvt.col_payoff_cum/num_games, mc_fvf.row_payoff_cum/num_games, mc_fvf.col_payoff_cum/num_games))
print("├───────────────────┼───────────────┼───────────────────┼───────────────┼───────────────┤")
print("│       Bully       │ ({:.3f},{:.3f}) │   ({:.3f},{:.3f})   │ ({:.3f},{:.3f}) │               │".format(mc_bvt.row_payoff_cum/num_games, mc_bvt.col_payoff_cum/num_games, mc_bvf.row_payoff_cum/num_games, mc_bvf.col_payoff_cum/num_games, mc_bvb.row_payoff_cum/num_games, mc_bvb.col_payoff_cum/num_games))
print("├───────────────────┼───────────────┼───────────────────┼───────────────┼───────────────┤")
print("│     Godfather     │ ({:.3f},{:.3f}) │   ({:.3f},{:.3f})   │ ({:.3f},{:.3f}) │ ({:.3f},{:.3f}) │".format(mc_gvt.row_payoff_cum/num_games, mc_gvt.col_payoff_cum/num_games, mc_gvf.row_payoff_cum/num_games, mc_gvf.col_payoff_cum/num_games, mc_gvb.row_payoff_cum/num_games, mc_gvb.col_payoff_cum/num_games, mc_gvg.row_payoff_cum/num_games, mc_gvg.col_payoff_cum/num_games))
print("└───────────────────┴───────────────┴───────────────────┴───────────────┴───────────────┘\n")