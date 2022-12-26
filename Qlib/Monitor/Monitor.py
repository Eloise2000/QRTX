from Qlib.Knowledge.Knowledge import instance as knowledge_instance
from rtxlib import process,error,info

class Monitor:

    def __init__(self, wf, ignore_size, sample_size):
        self.wf = wf
        self.ignore_size = ignore_size
        self.sample_size = sample_size

    def primary_data_reducer(self, cnt, newData):
        knowledge_instance.avg_overhead = (knowledge_instance.avg_overhead * cnt + newData["overhead"]) / (cnt + 1)
        knowledge_instance.total_complaint += newData["complaint"]
        knowledge_instance.avg_overhead_list.append(knowledge_instance.avg_overhead)
        knowledge_instance.total_complaint_list.append(knowledge_instance.total_complaint)
        return knowledge_instance.avg_overhead, knowledge_instance.total_complaint

    def run(self):
        if knowledge_instance.is_change_applied:
            # remove all old data from the queues
            self.wf.primary_data_provider["instance"].reset()

            avg_overhead = 0.0
            total_complaint = 0

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
            except StopIteration:
                # this iteration should stop asap
                error("This experiment got stopped as requested by a StopIteration exception")
            info("*** sum of complaint:   " + str(total_complaint))
            info("*** average overhead:   " + str(avg_overhead))
        else:
            None