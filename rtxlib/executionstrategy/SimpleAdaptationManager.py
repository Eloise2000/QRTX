from colorama import Fore

from rtxlib import info, error
from rtxlib.execution import experimentFunction

NUMBER_OF_DIMMER_LEVELS = 5
DIMMER_STEP = 1.0/ (NUMBER_OF_DIMMER_LEVELS - 1)
RT_THRESHOLD = 0.75
PERIOD = 60
import time



def start_simple_am(wf):
    """ executes forever - changes must come from definition file """
    info("> ExecStrategy   | simple_am ", Fore.CYAN)
    wf.totalExperiments = -1

    server_state = effector(wf, 'initial')

    while True:
        # server_state = effector(wf, '')
        
        response_time = 0
        
        print("current state:\n")
        print(server_state)
        print("end")

        if(not server_state):
            print("No more connection")
            wf.close_socket()
            return
        
        try:
            dimmer = float(server_state.get('dimmer'))
            response_time = float(server_state.get('average_rt'))
            activeServers = float(server_state.get("active_servers"))
            servers = float(server_state.get("servers"))
            max_servers = float(server_state.get("max_servers"))
            total_util = server_state.get("total_util")
            #["dimmer", "servers", "active_servers", "basic_rt", "optional_rt", "basic_throughput", "opt_throughput"]
            is_server_boot = (servers > activeServers)
            print("Is server boot?: " + str(is_server_boot))
        except: 
            continue



        if(response_time > RT_THRESHOLD):
            if( (not is_server_boot) and servers < max_servers ):
                server_state = effector(wf, "add_server")
            elif(dimmer > 0.0):
                new_dimmer = max(0.0, dimmer - DIMMER_STEP)
                server_state = effector(wf, "set_dimmer " + str(new_dimmer))
            else: server_state = effector(wf, 'data')
        elif(response_time < RT_THRESHOLD):
            spare_util = activeServers - total_util

            if(spare_util > 1):
                if(dimmer < 1.0):
                    new_dimmer = min(1.0, dimmer + DIMMER_STEP)
                    server_state = effector(wf, "set_dimmer " + str(new_dimmer))
                elif( (not is_server_boot) and servers > 1):
                    server_state = effector(wf, "remove_server")
                else: server_state = effector(wf, 'data')
            else: server_state = effector(wf, 'data')
        else: server_state = effector(wf, 'data')
        







def effector(wf, action):
    print("\n\n\n\n\nEffecting action " + action + "\n\n\n\n\n")
    wf.primary_data_provider["last_action"] = action.split()[0]
    return experimentFunction(wf, {
                "knobs": action,
                "ignore_first_n_results": wf.execution_strategy["ignore_first_n_results"],
                "sample_size": wf.execution_strategy["sample_size"]
            })