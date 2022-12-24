from colorama import Fore
from rtxlib.execution import experimentFunction
from rtxlib import info, error
import numpy as np
import time
import pickle
import statistics
from random import sample


DISCOUNT_FACTOR_GAMMA = 0.98

XI = 2


LIST_OF_GAMES = []

ARMS = []


def start_mab_discount_ucb_strategy(wf):
    """Uses the Discount UCB algorithm to determine best action from list given in knobs"""
    info("> ExecStrategy   | MAB Discounted Upper Confidence Bound", Fore.CYAN)
    
    wf.execution_strategy["isExperimentValid"] = False

    wf.totalExperiments = -1 #foreveR?

    global LIST_OF_GAMES
    

    dummy_rewards = [0.4, 0.2, 0.4, 0.4, 0.3, 0.9, 0.1, 0.5, 0.3, 0.5, 0.4, 0.1, 0.3, 0.3, 0.3, 0.3, 0.2, 0.5, 0.6, 0.6, 0.6]


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
    
    arm_counts = [0] * 21
    #reporting variables
    index_picks = []
    number_of_switches = 0
    all_rewards = []
    time_stamps = []
    #end
    
    while(int(time.perf_counter()) < 3600):#not any(arm_count > 590 for arm_count in arm_counts ) ):
        action_index = choose_action()
        time_stamp = str(int(time.perf_counter()))
        print("Time elapsed (seconds): " + time_stamp)
        # highest = max(arm_counts)
        # print("Highest: " + str(highest))

        # if(highest % 100 == 0):
        #     milestone_file = open('milestone' + str(highest) + '.txt', 'w')
        #     for index in index_picks:
        #         milestone_file.write("%s " % str(index))

        #     milestone_file.write("\n")

        #     for reward in all_rewards:
        #         milestone_file.write("%s " % str(reward))
            
        #     milestone_file.close()

        
            


        time_stamps.append(time_stamp)

        index_picks.append(action_index)

        arm_counts[action_index]+=1
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
    
    results_file = open('98_s10_img_to_text_abrupt30.txt', 'w')

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
    global DISCOUNT_FACTOR_GAMMA
    best_arm = None
    best_value = -9999999


    for arm_index in range(len(ARMS)):
        current_value = X_t(DISCOUNT_FACTOR_GAMMA,arm_index) + c_t(DISCOUNT_FACTOR_GAMMA, arm_index)

        #print("Value at " + str(arm_index) + " is " + str(current_value))
        if(current_value > best_value):
            best_value = current_value
            best_arm = arm_index
    

    #print("Picked " + str(best_arm))
    return best_arm





def N_t(gamma, i):
    global LIST_OF_GAMES

    #print("discount is " + str(discount))
    total_count = len(LIST_OF_GAMES)

    sum_of_uses = 0
    for game_index in range(total_count):
        if(LIST_OF_GAMES[game_index][1] == i): #I_s == i in other words arm of game equals given arm
            #print("game index is " + str(game_index))
            factor = gamma**(total_count - game_index) #discount_factor ^ t-s
            #print("factor is " + str(factor) )
            #print("The factor is " + str(factor))
            sum_of_uses += factor

    return sum_of_uses

def X_t(gamma, i):
    global LIST_OF_GAMES

    discount = gamma

    total_count = len(LIST_OF_GAMES)

    #print("The total count is " + str(total_count)) 
    sum_of_rewards = 0.0
    for game_index in range(total_count): #s through t
        current_game = LIST_OF_GAMES[game_index]
        if(current_game[1]  == i):
            factor = discount**(total_count - game_index) #gamma ^ t-s

            sum_of_rewards+= float(factor * current_game[0]) #discount factor * reward at moment s of arm i
            

    return sum_of_rewards/N_t(discount,i)

def n_t(gamma):
    global ARMS
    all_count = 0.0
    for arm_index in range(len(ARMS)):
        all_count+=N_t(gamma,arm_index)
    
    return all_count

def c_t(gamma, i):
    global XI
    global LIST_OF_GAMES
    #2B sqrt(xi * log(nt(gamma))/N_t(gamma,i)

    #regular = IEEESASO2019(i,n_t(gamma))

    
    top = XI * np.log(n_t(gamma)) # 2 * ln( n_t(gamma) )
    #print("top is " + str(top) + "log of " + str(n_t(gamma)))
    to_be_root = top/N_t(gamma,i) #2ln(n) / n_k
    #print("to_be_root " + str(to_be_root))
    RHS = to_be_root * 0.25 # 0.25(2(ln(n))/n_k)

    B = np.log(n_t(gamma)) / N_t(gamma,i)
    #print("B is " + str(B))
    LHS = 2 * B

    #print("LHS is " + str(LHS))
    #print("RHS is " + str(RHS))
    res = np.sqrt(LHS * RHS)

    #print("these two values should be the same " + str(res) + " " + str(regular) )

    return res

def IEEESASO2019(i, n):
    "Function from the IEEE SASO 2019 paper by Porter and Rodrigues"
    constant = 0.25

    n_k = N_t(DISCOUNT_FACTOR_GAMMA,i)

    ln_n = np.log(n)

    left_term = (ln_n/n_k) * constant

    left_term = 2 * left_term
    right_term = ((2.0 * ln_n) /n_k)
    
    return np.sqrt(left_term * right_term)
    





    
    




