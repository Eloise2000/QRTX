import csv
from rtxlib import error
def log_results(experiment_folder, round, total_complaints, append=True):
    """ logs the result values of an experiment to a csv file """
    try:
        data_list = []
        for r, c in zip(round, total_complaints):
            x = {}
            x['round'] = r
            x['complaint'] = c
            data_list.append(x)

        if append:
            with open('./' + str(experiment_folder) + '/results.csv', 'a+') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                writer.writerow(['round', 'number of complaints'])
                for val in data_list:
                    writer.writerow(val.values())
        else:
            with open('./' + str(experiment_folder) + '/results.csv', 'w+') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                writer.writerow(['round', 'number of complaints'])
                for val in data_list:
                    writer.writerow(val.values())

    except csv.Error as e:
        error("Log to csv did not work: " + str(e))
        pass