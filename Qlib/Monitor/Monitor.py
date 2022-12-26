from Qlib.Knowledge.Knowledge import instance as knowledge_instance
from rtxlib import process,error,info

class Monitor:

    def __init__(self, wf, ignore_size, sample_size):
        self.wf = wf
        self.ignore_size = ignore_size
        self.sample_size = sample_size
        self.avg_overhead = 0
        self.total_complaint = 0

    def primary_data_reducer(self, cnt, newData):
        self.avg_overhead = (self.avg_overhead * cnt + newData["overhead"]) / (cnt + 1)
        self.total_complaint += newData["complaint"]
        return self.avg_overhead, self.total_complaint

    def run(self):
        # remove all old data from the queues
        self.wf.primary_data_provider["instance"].reset()

        self.avg_overhead = 0
        self.total_complaint = 0

        # ignore samples to wait the effect of the change
        if self.ignore_size > 0:
            i = 0
            while i < self.ignore_size:
                new_data = self.wf.primary_data_provider["instance"].returnData()
                if new_data is not None:
                    i += 1
                    process("IgnoreSamples  | ", i, self.ignore_size)
            print("")

        # start collecting data
        i = 0
        try:
            while i < self.sample_size:
                new_data = self.wf.primary_data_provider["instance"].returnData()
                if new_data is not  None:
                    try:
                        avg_overhead, total_complaint = self.primary_data_reducer(i, new_data)
                    except StopIteration:
                        raise StopIteration()  # just fwd
                    except RuntimeError:
                        raise RuntimeError()  # just fwd
                    except:
                        error("could not reducing data set: " + str(new_data))
                    i += 1
                    process("CollectSamples | ", i, self.sample_size)
            print("")
            knowledge_instance.avg_overhead = self.avg_overhead
            knowledge_instance.total_complaint = self.total_complaint
            knowledge_instance.avg_overhead_list.append(knowledge_instance.avg_overhead)
            knowledge_instance.total_complaint_list.append(knowledge_instance.total_complaint)
            knowledge_instance.episode += 1
            info("*** sum of complaint:   " + str(total_complaint))
            info("*** average overhead:   " + str(avg_overhead))
        except StopIteration:
            # this iteration should stop asap
            error("This experiment got stopped as requested by a StopIteration exception")

