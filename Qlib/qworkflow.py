from colorama import Fore

from rtxlib import info, error
from rtxlib.changeproviders import init_change_provider
from rtxlib.dataproviders import init_data_providers
from rtxlib.preprocessors import init_pre_processors, kill_pre_processors
from Qlib.Monitor.Monitor import Monitor
from Qlib.Executor.Executor import Executor

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
    executor = Executor(wf)

    #MAPE-K loop
    info("> MAPE-K running......")
    monitor.run()
    executor.run()
    # we are done, now we clean up
    kill_pre_processors(wf)
    info("> Finished workflow")