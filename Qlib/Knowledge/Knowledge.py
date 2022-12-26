import numpy as np


class Knowledge:
    def __init__(self):
        self.state_size = 50 # [0,50], step 1
        self.action_size = 30 # [0,0.6], step 0.02
        self.q_table = np.random.uniform(low=-1, high=1, size=(self.state_size, self.action_size)) # q_table[state][action]

        self.avg_overhead = 0.0
        self.total_complaint = 0
        self.avg_overhead_list = []
        self.total_complaint_list = []

        self.episode = 0
        self.action = None # action of last round, update after planner
        self.new_knob_val = None

        self.training_round = 0

instance = Knowledge()