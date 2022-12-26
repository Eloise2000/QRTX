from rtxlib import error, info
from Qlib.Knowledge.Knowledge import instance as knowledge_instance
import numpy as np

class Planner:
    def __init__(self):
        return

    def run(self):
        if knowledge_instance.action is None:
            knowledge_instance.action = np.random.choice(np.arange(0,0.6,0.02))
        knowledge_instance.new_knob_val = {"exploration_percentage": knowledge_instance.action}
        info("> Current knob value is: " + str(knowledge_instance.new_knob_val))