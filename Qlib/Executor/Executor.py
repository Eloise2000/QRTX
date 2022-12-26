from rtxlib import error, info
from Qlib.Knowledge.Knowledge import instance as knowledge_instance

class Executor:
    def __init__(self, wf):
        self.wf = wf


    def _defaultChangeProvider(self, variables):
        """ by default we just forword the message to the change provider """
        return variables

    def run(self):
        # apply changes to system
        try:
            self.wf.change_provider["instance"].applyChange(self._defaultChangeProvider(knowledge_instance.new_knob_val))
        except:
            error("apply changes did not work")

        info("< new exploration percentage applied: " + str(knowledge_instance.new_knob_val))