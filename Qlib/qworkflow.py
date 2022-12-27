from colorama import Fore
import numpy as np

from rtxlib import info, error
from rtxlib.changeproviders import init_change_provider
from rtxlib.dataproviders import init_data_providers
from rtxlib.preprocessors import init_pre_processors, kill_pre_processors
from Qlib.Monitor.Monitor import Monitor
from Qlib.Executor.Executor import Executor
from Qlib.Analyser.Analyser import Analyser
from Qlib.Planner.Planner import Planner
from Qlib.Knowledge.Knowledge import instance as knowledge_instance
from Qlib import log_results, save_qtable
from Qlib.report import plot

def test_qworkflow(wf, path):
    """ here test the trained q-table """

    info("######################################", Fore.CYAN)
    info("> Testing on   | " + str(wf.name), Fore.CYAN)

    q_table = np.loadtxt(path, delimiter=",")
    knowledge_instance.q_table = q_table

    # initialize the test environment
    init_pre_processors(wf)
    init_change_provider(wf)
    init_data_providers(wf)

    # Set up all variables
    ignore_size = 10
    sample_size = 10
    rounds = 3
    plot_idx = 3

    monitor = Monitor(wf,ignore_size,sample_size)
    analyser = Analyser()
    planner = Planner()
    executor = Executor(wf)

    # MAPE-K loop
    info("> MAPE-K running......")
    for i in range(rounds):
        info(">  episode: "+str(i+1)+"/"+str(rounds))
        monitor.run()
        analyser.run(True) # test_flag = True -> test
        planner.run()
        executor.run()
    
    info("> test" + str(knowledge_instance.total_complaint_list))
    log_results(wf.folder, [n+1 for n in range(rounds)], knowledge_instance.total_complaint_list,
                knowledge_instance.avg_overhead_list, knowledge_instance.reward_list,False)
    plot(wf,plot_idx)

    # we are done, now we clean up
    kill_pre_processors(wf)
    info("> Finished test workflow")

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

    # Set up all variables
    ignore_size = 10
    sample_size = 10
    rounds = 3
    flag = 1 # 1 is q-learning, 0 is random
    plot_idx = 3

    monitor = Monitor(wf,ignore_size,sample_size)
    analyser = Analyser()
    planner = Planner()
    executor = Executor(wf)

    if flag:
        # MAPE-K loop
        info("> MAPE-K running......")
        for i in range(rounds):
            info(">  episode: "+str(i+1)+"/"+str(rounds))
            monitor.run()
            analyser.run(False) # test_flag = False -> train
            planner.run()
            executor.run()
        # Save q-table
        info("> Saving Q table......")
        save_qtable(wf.folder)
    else:
        # Random select action
        info("> Random action running......")
        for i in range(rounds):
            info(">  episode: "+str(i+1)+"/"+str(rounds))
            monitor.run()
            reward = analyser.compute_reward()
            knowledge_instance.reward_list.append(reward)
            knowledge_instance.new_knob_val = {"exploration_percentage": np.random.choice(np.arange(0,0.6,0.02))}
            executor.run()
        
    info("> test" + str(knowledge_instance.total_complaint_list))
    log_results(wf.folder, [n+1 for n in range(rounds)], knowledge_instance.total_complaint_list,
                knowledge_instance.avg_overhead_list, knowledge_instance.reward_list,False)
    plot(wf,plot_idx)

    # we are done, now we clean up
    kill_pre_processors(wf)
    info("> Finished workflow")