from rtxlib import error, info
from Qlib.Knowledge.Knowledge import instance as knowledge_instance
import numpy as np

class Analyser:
    def __init__(self):
        self.alpha = 0.2
        self.gamma = 0.99

    def compute_reward(self):
        reward = -(100 * (knowledge_instance.avg_overhead - 2.5) + knowledge_instance.total_complaint)
        info("**** Reward: "+ str(reward))
        return reward

    def run(self):
        if knowledge_instance.action: # if have last state
            last_state_q = knowledge_instance.total_complaint_list[-2]
            last_action_q = int(knowledge_instance.action * 50)
            reward = self.compute_reward()
            state_q = knowledge_instance.total_complaint
            action_q = np.argmax(knowledge_instance.q_table[last_state_q])
            # update q-table
            knowledge_instance.q_table[last_state_q][last_action_q] = (1 - self.alpha) * knowledge_instance.q_table[last_state_q][last_action_q] + self.alpha * (reward + self.gamma * knowledge_instance.q_table[state_q][action_q])
        