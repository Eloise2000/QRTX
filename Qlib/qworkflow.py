from colorama import Fore

from rtxlib import info, error
from rtxlib.changeproviders import init_change_provider
from rtxlib.dataproviders import init_data_providers
from rtxlib.preprocessors import init_pre_processors, kill_pre_processors
from Qlib.Monitor.Monitor import Monitor
from Qlib.Executor.Executor import Executor
from Qlib.Analyser.Analyser import Analyser
from Qlib.Planner.Planner import Planner
from Qlib.Knowledge.Knowledge import instance as knowledge_instance
from Qlib import log_results
from Qlib.report import plot

# init change_provider, data_provider and execute MAPE-K loop
def execute_workflow(wf):
    """ this is the main workflow for executing a given workflow """
    try:
        # check that the definition is correct
        info("######################################", Fore.CYAN)
        info("> Workflow       | " + str(wf.name), Fore.CYAN)
        # check variables
        b = wf.change_provider
        c = wf.primary_data_provider
    except KeyError as e:
        error("definition.py is missing value " + str(e))
        exit(1)
    # initialize the test environment
    init_pre_processors(wf)
    init_change_provider(wf)
    init_data_providers(wf)

    monitor = Monitor(wf,100,100)
    analyser = Analyser()
    planner = Planner()
    executor = Executor(wf)

    round = 30
    #MAPE-K loop
    info("> MAPE-K running......")
    for i in range(round):
        info(">  episode: "+str(i)+"/"+str(round))
        monitor.run()
        analyser.run()
        planner.run()
        executor.run()

    log_results(wf.folder, [n+1 for n in range(round)], knowledge_instance.total_complaint_list,
                knowledge_instance.avg_overhead_list, knowledge_instance.reward_list,False)
    plot(wf,1)


    # we are done, now we clean up
    kill_pre_processors(wf)
    info("> Finished workflow")