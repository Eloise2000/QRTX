from colorama import Fore

from rtxlib import info, error
from rtxlib.execution import experimentFunction
from python_ews import global_vars
from python_ews.server_interface import ewsRESTInterface as eRI
from python_ews.modelling import ConfigurationModel


#uses http to determine sequential configurations at runtime
def start_seq_runtime_stategy(wf):
    """ executes all experiments from the definition file """
    info("> ExecStrategy   | SequentialRuntimeConfigs", Fore.CYAN)



    retrieve_true_knobs(wf)



    #the regular sequential code starts here
    wf.totalExperiments = len(wf.execution_strategy["knobs"])
    for kn in wf.execution_strategy["knobs"]:
        experimentFunction(wf, {
            "knobs":kn,
            "ignore_first_n_results": wf.execution_strategy["ignore_first_n_results"],
            "sample_size": wf.execution_strategy["sample_size"],
        })


def retrieve_true_knobs(wf):
    knobs = wf.execution_strategy["knobs"][0]

    print(type(wf.execution_strategy))
    if "source" in knobs:

        config_model = ConfigurationModel()
        

        list_rel_w_alt = config_model.relations_with_alternatives()


        for rel_w_alt in list_rel_w_alt:
            rel_alts = config_model.relation_alternative(rel_w_alt)

            rel_alts.append(rel_w_alt)

            values = []
            for alt in rel_alts:
                values.append(alt.child_comp)
            
            variable = {rel_w_alt.get_name() : values}


            wf.execution_strategy["knobs"].append(variable)

        print(wf.execution_strategy["knobs"])

        global_vars.IP = "wrong" #knobs["source"] #this doesn't work
        configs = eRI.get_all_configs()
        wf.execution_strategy["knobs"].clear()


        for config_obj in configs:
            wf.execution_strategy["knobs"].append({"config":config_obj.original_json})
    else:
        error("source of configurations not included")
        exit(1)
