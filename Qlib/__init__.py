import csv
from rtxlib import error
import numpy as np
from Qlib.Knowledge.Knowledge import instance as knowledge_instance

def save_qtable(experiment_folder):
    """ save qtable to a csv file """
    np.savetxt('./' + str(experiment_folder) + "/q_table.csv", knowledge_instance.q_table, delimiter=",")

def log_results(experiment_folder, round, total_complaints, trip_overheads, rewards, append=True):
    """ logs the result values of an experiment to a csv file """
    try:
        data_list = []
        for r, c, o, w in zip(round, total_complaints, trip_overheads, rewards):
            x = {}
            x['round'] = r
            x['complaint'] = c
            x['overhead'] = o
            x['reward'] = w
            data_list.append(x)

        if append:
            with open('./' + str(experiment_folder) + '/results.csv', 'a+') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                writer.writerow(['round', 'number of complaints','avg overhead','reward'])
                for val in data_list:
                    writer.writerow(val.values())
        else:
            with open('./' + str(experiment_folder) + '/results.csv', 'w+') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                writer.writerow(['round', 'number of complaints','avg overhead','reward'])
                for val in data_list:
                    writer.writerow(val.values())

    except csv.Error as e:
        error("Log to csv did not work: " + str(e))
        pass