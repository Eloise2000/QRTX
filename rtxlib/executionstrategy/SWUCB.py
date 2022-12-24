from colorama import Fore
from rtxlib.execution import experimentFunction
from rtxlib import info, error
import numpy as np
import time
import pickle
from random import sample
import statistics

ACTION = 0
REWARD = 1
N_K = 2

LOOK_BACK = 250 #150  #50, 150, 300

LIST_OF_GAMES = []

ARMS = []

XI = 2

def start_mab_sw_ucb_strategy(wf):
    """Uses the UCB algorithm to determine best action from list given in knobs"""
    info("> ExecStrategy   | MAB Sliding Window Upper Confidence Bound", Fore.CYAN)
        
    wf.execution_strategy["isExperimentValid"] = False

    wf.totalExperiments = -1 #foreveR?

    global LIST_OF_GAMES
    
    #the arms should could from knobs
    ARMS.extend(wf.execution_strategy["knobs"]) #i.e. the actions/action space
    #Parameters, including global values, are read only, unless they are mutable, then through mutation methods they can be changed, but not through assignment



    #action_reward_pairs = [ [arm, 0.0, 0.0] for arm in arms ] 

    #(arm, reward, count)
    #(action, reward, n_k)

    #establish base rewards
    for arm_index in range(len(ARMS)):
        print("army")
        wf.execution_strategy["isExperimentValid"] = False
        print("experiment valid false now after army")

        collected_values = []
       
        get_results(collected_values,wf, ARMS[arm_index])

        LIST_OF_GAMES.append((statistics.mean(collected_values), arm_index)) #this represents the return of the evaluator() in definition.py and may need to be adjusted.
    
    print("finished establishing base values")
    
    
    #reporting variables
    index_picks = []
    number_of_switches = 0
    all_rewards = []
    time_stamps = []
    #end
    
    while(int(time.perf_counter()) < 3600):
        action_index = choose_action()
        time_stamp = str(int(time.perf_counter()))
        print("Time elapsed (seconds): " + time_stamp)



        time_stamps.append(time_stamp)

        index_picks.append(action_index)

        current_action = ARMS[action_index]

        results = []

        get_results(results,wf,current_action)

        reward = statistics.mean(results)
        
        # if(int(time_stamp) > 1800):
        #     print("POST SWITCH\n")
        #     if(action_index in [2,3,10,11,12,13,14]):
        #         print("GZIP IMPROVED \n")
        #         reward = 1.0
            
        LIST_OF_GAMES.append((reward,action_index))

        all_rewards.append(reward)

        number_of_switches+=1
    
    results_file = open('s10_imgtotext_250sw_abrupt30min_1hour.txt', 'w')

    for index in index_picks:
        results_file.write("%s " % str(index))

    results_file.write("\n")

    for reward in all_rewards:
        results_file.write("%s " % str(reward))

    results_file.write("\n")

    for stamp in time_stamps:
        results_file.write("%s " % str(stamp))

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
                "sample_size": wf.execution_strategy["sample_size"],
            })


def choose_action():
    global ARMS
    global LOOK_BACK
    best_arm = None
    best_value = -9999999


    for arm_index in range(len(ARMS)):
        current_value = X_t(LOOK_BACK,arm_index) + c_t(LOOK_BACK, arm_index)
        if(current_value > best_value):
            best_value = current_value
            best_arm = arm_index
    
    return best_arm





def N_t(tau, i):
    global LIST_OF_GAMES

    #print("discount is " + str(discount))
    total_count = len(LIST_OF_GAMES) #t
    
    start_point = max(0, total_count-tau+1)
    count = 0
    for game_index in range(start_point,total_count):
        if(LIST_OF_GAMES[game_index][1] == i): #I_s == i in other words arm of game equals given arm
            count += 1

    return count

def X_t(tau, i):
    global LIST_OF_GAMES
    total_count = len(LIST_OF_GAMES) #t
    summated = 0

    start_point = max(0, total_count-tau+1)
    for game_index in range(start_point,total_count):
        current_game = LIST_OF_GAMES[game_index]
        if(current_game[1] == i): #the games in which i was the arm
            X_s = current_game[0]

            summated+=X_s

    return summated/N_t(tau,i)
    
def c_t(tau, i):
    global XI
    global LIST_OF_GAMES
    

    t = len(LIST_OF_GAMES)
    
    t_or_tau = min(t,tau)


    B = np.log(t_or_tau) / N_t(tau,i)

    

    frac_top = XI * np.log(t_or_tau)

    frac_bot = N_t(tau,i)

    RHS = (frac_top / frac_bot) * 0.25

    res = np.sqrt(B * RHS)

    return res
 