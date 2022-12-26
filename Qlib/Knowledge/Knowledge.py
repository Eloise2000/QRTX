


class Knowledge:



    def __init__(self, change_applied, avg_overhead, total_complaint):
        self.is_change_applied = change_applied
        self.avg_overhead = avg_overhead
        self.total_complaint = total_complaint
        self.avg_overhead_list = []
        self.total_complaint_list = []

        self.training_round = 0
        self.new_knob_val = 0.0


instance = Knowledge(True, 0.0, 0)