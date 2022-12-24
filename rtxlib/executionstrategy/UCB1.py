from colorama import Fore
from rtxlib.execution import experimentFunction
from rtxlib import info, error
import numpy as np
import time
import pickle
from random import sample

ACTION = 0
REWARD = 1
N_K = 2

FORMULA_FUNC = None

def start_mab_ucb1_strategy(wf):
    """Uses the UCB algorithm to determine best action from list given in knobs"""
    info("> ExecStrategy   | MAB Upper Confidence Bound", Fore.CYAN)
    
    wf.execution_strategy["isExperimentValid"] = False
 

    #retrieve_true_knobs(wf)
    print(len(wf.execution_strategy["knobs"]))
    #exit(0)
    wf.totalExperiments = -1 #foreveR?

    formula = wf.execution_strategy["formula"]
    global FORMULA_FUNC
    FORMULA_FUNC = formula_to_function(formula) #this shouldn't be done every time

    #Reward comes from experiment execution
    #Regret is sqrt( (ln(n)/n_k) * 0.25 * (2ln(n)/n_k) )
    #sqrt( (np.log(n)/n_k) * 0.25 * ( (2 * np.log(n))/n_k) ) )
    #Pick k (from arms) with highest Reward + Regret


    dummy_rewards = [0.4, 0.2, 0.4, 0.4, 0.3, 0.9, 0.1, 0.5, 0.3, 0.5, 0.4, 0.1, 0.3, 0.3, 0.3, 0.3, 0.2, 0.5, 0.6, 0.6, 0.6]


    total_count = 0 #n
  

    #the arms should could from knobs
    arms = wf.execution_strategy["knobs"] #i.e. the actions/action space

    action_reward_pairs = [ [arm, 0.0, 0.0] for arm in arms ] 

    #(arm, reward, count)
    #(action, reward, n_k)

    #establish base rewards
    for pair in action_reward_pairs:
        print("army")
        wf.execution_strategy["isExperimentValid"] = False
        print("experiment valid false now after army")

        collected_values = []
       
        get_results(collected_values,wf,pair[ACTION])

        pair[REWARD] = pair[REWARD] + sum(collected_values) #this represents the return of the evaluator() in definition.py and may need to be adjusted.
        
        pair[N_K] = pair[N_K] + float(wf.execution_strategy["sample_points"])
        total_count+= float(wf.execution_strategy["sample_points"])

    
    print("finished establishing base values")
    
    
    #reporting variables
    index_picks = []
    number_of_switches = 0
    all_rewards = []
    #end
    
    while(number_of_switches < 5001):
        action_index = choose_action(wf,action_reward_pairs,total_count)
        print("switch: %s action_index: %s " % (number_of_switches, action_index))
        index_picks.append(action_index)


        current_action = action_reward_pairs[action_index]

        results = []

        get_results(results,wf,current_action[ACTION])

        result_sum = sum(results)
        current_action[REWARD] = current_action[REWARD] + result_sum
        all_rewards.append(result_sum)
        current_action[N_K] = current_action[N_K] + float(wf.execution_strategy["sample_points"])
        
        total_count+= float(wf.execution_strategy["sample_points"])
        number_of_switches+=1
    
    results_file = open('resultsUCB12000.txt', 'w')

    for index in index_picks:
        results_file.write("%s " % str(index))

    results_file.write("\n")

    for reward in all_rewards:
        results_file.write("%s " % str(reward))

    results_file.close()


def get_results(values_to_collect, wf, action):
    while(True): 
        #this loop was added to deal with no_metric or ValueError
        time.sleep(wf.execution_strategy["collection_window"])

        result = arm_experiment(wf,action)

        values_to_collect.extend(result)  
        if(wf.execution_strategy["isExperimentValid"]):
            break
        else:
            if len(values_to_collect) >= wf.execution_strategy["sample_points"]:
                break

        #result = (dummy_rewards[pair_count],0)
    sample_list = sample(values_to_collect, wf.execution_strategy["sample_points"])
    values_to_collect.clear()
    values_to_collect.extend(sample_list)



def arm_experiment(wf, arm):
    return experimentFunction(wf, {
                "knobs": {"config": arm},
                "ignore_first_n_results": wf.execution_strategy["ignore_first_n_results"],
                "sample_size": wf.execution_strategy["sample_size"]
            })



def formula_to_function(choice):
    funcs = {
            "IEEESASO2019": IEEESASO2019,
        }
         
    func = funcs.get(choice)
    #print(func.__doc__)
    return func

def choose_action(wf,pairs, n):
    "Returns index in the pair list of the chosen action"

   


    highest = -99999999 # - sys.maxsize perhaps (python3 is unbounded)
    chosen_action = None

    for pair_index in range(len(pairs)):

        current_pair = pairs[pair_index]

        Q_a = current_pair[REWARD]/current_pair[N_K]
    
    
        confidence = FORMULA_FUNC(current_pair, n)

        result = Q_a + confidence

        if(result > highest):
            highest = result
            chosen_action = pair_index

    print("the value was " + str(highest))
    return chosen_action


    #sqrt( (np.log(n)/n_k) * 0.25 * ( (2 * np.log(n))/n_k) ) )

    
def IEEESASO2019(pair, n):
    "Function from the IEEE SASO 2019 paper by Porter and Rodrigues"
    constant = 0.25

    a_r_nk = pair
    n_k = a_r_nk[N_K]

    ln_n = np.log(n)

    left_term = ln_n/n_k

    right_term = constant * ((2.0 * ln_n) /n_k)
    
    return np.sqrt(left_term * right_term)


    
    




