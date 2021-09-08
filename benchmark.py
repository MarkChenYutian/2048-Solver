import os
import json
import time

from emulator.emulator_core import GameOverException

from greedyAgent import GreedyAgent
from geneticAlgorithmAgent import GeneticAlgorithmAgent
from treeEvaluateAgent import TreeEvaluateAgent

if __name__ == "__main__":
    # Initialize your agent as a key-value pair here (Name - Agent Object)
    agentLib = {
        "Greedy_Agent": GreedyAgent(),
        "GA_Agent": GeneticAlgorithmAgent(fromAgent=[], paramDict={
            "empty_tile_weight": 1.0388513188766846,
            "max_tile_weight": 1.217110527336104,
            "up_preference": 1.1857577900193952,
            "down_preference": 0.9060732062418375,
            "left_preference": 0.7893698799635284,
            "right_preference": 0.10917351624666222
        }),
        "Tree_Agent": TreeEvaluateAgent()
    }

    # SETUP AREA #################################
    # Set agent you want to test
    testAgent = agentLib["Tree_Agent"]
    # Start testing from ...
    START_FROM = 2000
    # End testing at ...
    FINAL_TARGET = 2001
    # If recovery mode is true, the benchmark result will be dumped after each evaluation
    # If the agent run fast, the dumping operation will significant slow benchmark down and 
    # it is advised NOT to open RECOVERY MODE in this situation.
    RECOVERY_MODE = True
    # Store state data for future research
    STORE_CASES = True
    AVG_PATH = "./storage/BenchmarkResult/tree_evaluator_average.json"
    RAW_PATH = "./storage/BenchmarkResult/tree_evaluator_rawData.json"
    ##############################################
    states = []
    result = []
    average = []
    curr_sum = 0
    if START_FROM != 0 and RECOVERY_MODE:
        with open(RAW_PATH, "r") as f:
            result = json.load(f)
        with open(AVG_PATH, "r") as f:
            average = json.load(f)
        curr_sum = sum(result)
    
    case = START_FROM
    while case < FINAL_TARGET:
        states = []
        timer_start = time.time()
        while True:
            if testAgent.stepCount > 2000: 
                print("Cut down due to Timeout.")
                case -= 1
                break
            try:
                testAgent.make_move(withGUI=True)
                states.append(testAgent.state)
            except GameOverException:
                score = sum([sum(row) for row in testAgent.state])
                result.append(score)
                curr_sum += score
                average.append(curr_sum / (case + 1))
                print(case, result[-1], " | ", int(average[-1]))
                break
        
        testAgent.clearState()

        if RECOVERY_MODE:
            with open(RAW_PATH, "w") as f:
                json.dump(result, f)
            with open(AVG_PATH, "w") as f:
                json.dump(average, f)
            
        if STORE_CASES:
            with open("./storage/treeEvaluateStates/game{}.json".format(case), "w") as f:
                json.dump(states, f)
        
        case += 1

    if not RECOVERY_MODE:
        with open(RAW_PATH, "w") as f:
            json.dump(result, f)
        with open(AVG_PATH, "w") as f:
            json.dump(average, f)
