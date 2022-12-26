from rtxlib import error, info
from Qlib.Knowledge.Knowledge import instance as knowledge_instance
import numpy as np

class Planner:
    def __init__(self):
        return

    def run(self):
        state_q = knowledge_instance.total_complaint
        next_action = np.argmax(knowledge_instance.q_table[state_q]) / 50
        knowledge_instance.action = next_action
        knowledge_instance.new_knob_val = {"exploration_percentage": next_action}
        info("> Current knob value is: " + str(knowledge_instance.new_knob_val))