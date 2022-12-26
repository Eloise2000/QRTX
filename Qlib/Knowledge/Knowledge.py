


class Knowledge:
    def __init__(self):
        self.avg_overhead = 0.0
        self.total_complaint = 0
        self.avg_overhead_list = []
        self.total_complaint_list = []

        self.training_round = 0
        self.new_knob_val = {"exploration_percentage": 0.5}


instance = Knowledge()