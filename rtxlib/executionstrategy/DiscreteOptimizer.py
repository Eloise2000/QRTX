from colorama import Fore
import requests
from skopt import gp_minimize
from rtxlib import info, error
from rtxlib.execution import experimentFunction

def start_discrete_optimizer_strategy(wf):
    """ executes a discrete value optimizing strategy """
    info("> ExecStrategy   | DiscreteOptimizer", Fore.CYAN)
    optimizer_method = wf.execution_strategy["optimizer_method"]
    wf.totalExperiments = wf.execution_strategy["optimizer_iterations"]
    optimizer_random_starts = wf.execution_strategy["optimizer_random_starts"]
    info("> Optimizer      | " + optimizer_method, Fore.CYAN)

    retrieve_true_knobs(wf)

    knobs = wf.execution_strategy["knobs"]
  
    list_categories = list(knobs[0].values())[0]

    print(type(list_categories))    


    # we give the minimization function a callback to execute
    # it uses the return value (it tries to minimize it) to select new knobs to test
    optimizer_result = gp_minimize(lambda opti_values: self_optimizer_execution(wf, opti_values),
                                   dimensions=list_categories, n_calls=wf.totalExperiments, n_random_starts=optimizer_random_starts)
    # optimizer is done, print results
    info(">")
    info("> OptimalResult  | Knobs:  " + str(recreate_knob_from_optimizer_values(variables, optimizer_result.x)))
    info(">                | Result: " + str(optimizer_result.fun))


def recreate_knob_from_optimizer_values(variables, opti_values):
    """ recreates knob values from a variable """
    knob_object = {}
    # create the knobObject based on the position of the opti_values and variables in their array
    for idx, val in enumerate(variables):
        knob_object[val] = opti_values[idx]
    return knob_object


def self_optimizer_execution(wf, opti_values):
    """ this is the function we call and that returns a value for optimization """
    print(opti_values) #need to see what this is
    #knob_object = recreate_knob_from_optimizer_values(variables, opti_values)
    # create a new experiment to run in execution
    # return experimentFunction(wf, {
    #         "knobs":knob_object,
    #         "ignore_first_n_results": wf.execution_strategy["ignore_first_n_results"],
    #         "sample_size": wf.execution_strategy["sample_size"],
    #     })
    exit(1)

    return 0

def retrieve_true_knobs(wf):
    knobs = wf.execution_strategy["knobs"][0]

    if "source" in knobs:

        wf.execution_strategy["knobs"].clear()

        #SOURCE SHOULD STILL BE LOADED IN (replace the IP used somehow)

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

        #global_vars.IP = "wrong" #knobs["source"] #this doesn't work
        #configs = eRI.get_all_configs()
        


        #for config_obj in configs:
        #   wf.execution_strategy["knobs"].append({"config":config_obj.original_json})
    else:
        error("source of configurations not included")
        exit(1)