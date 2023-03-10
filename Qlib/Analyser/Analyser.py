from rtxlib import error, info
from Qlib.Knowledge.Knowledge import instance as knowledge_instance
import numpy as np

class Analyser:
    def __init__(self):
        self.alpha = 0.35
        self.gamma = 0.99
        self.epsilon = 0.2

    def compute_reward(self):
        reward = -(100 * (knowledge_instance.avg_overhead - 2.5) + knowledge_instance.total_complaint)
        info("**** Reward: "+ str(reward))
        return reward

    def run(self, test_flag):
        # test_flag = True -> test
        if test_flag:
            state_q = knowledge_instance.total_complaint
            action = np.argmax(knowledge_instance.q_table[state_q]) / 50
            knowledge_instance.action = action
            reward = self.compute_reward()
            knowledge_instance.reward_list.append(reward)
        # test_flag = False -> train
        elif knowledge_instance.action is not None: # if have last state
            last_state_q = knowledge_instance.total_complaint_list[-2]
            last_action_q = int(knowledge_instance.action * 50)
            reward = self.compute_reward()
            knowledge_instance.reward_list.append(reward)
            state_q = knowledge_instance.total_complaint
            if self.epsilon <= np.random.uniform(0, 1):
                action_q = np.argmax(knowledge_instance.q_table[state_q])
                action = action_q / 50
            else:
                action_q = np.random.choice(knowledge_instance.action_size)
                action = action_q / 50
            knowledge_instance.action = action
            # update q-table
            knowledge_instance.q_table[last_state_q][last_action_q] = (1 - self.alpha) * knowledge_instance.q_table[last_state_q][last_action_q] + self.alpha * (reward + self.gamma * knowledge_instance.q_table[state_q][action_q])
            # decrease epsilon
            self.epsilon = 0.5 * (0.99 ** knowledge_instance.episode)
        