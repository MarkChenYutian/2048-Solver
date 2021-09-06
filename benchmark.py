import json

from emulator.emulator_core import GameOverException
from emulator.emulator_api import get_max_tile

from greedyAgent import GreedyAgent
from geneticAlgorithmAgent import GeneticAlgorithmAgent
from treeEvaluateAgent import TreeEvaluateAgent

if __name__ == "__main__":
    agentLib = {
        "GA_Agent": GeneticAlgorithmAgent(fromAgent=[], paramDict={
            "empty_tile_weight": 1.0388513188766846,
            "max_tile_weight": 1.217110527336104,
            "up_preference": 1.1857577900193952,
            "down_preference": 0.9060732062418375,
            "left_preference": 0.7893698799635284,
            "right_preference": 0.10917351624666222
        }),
        "Greedy_Agent": GreedyAgent(),
        "Tree_Agent": TreeEvaluateAgent()
    }

    testAgent = agentLib["Tree_Agent"]
    result = []
    average = []
    curr_sum = 0
    for case in range(200):
        while True:
            try:
                testAgent.make_move(withGUI=True)
            except GameOverException:
                score = sum([sum(row) for row in testAgent.state])
                result.append(score)
                curr_sum += score
                average.append(curr_sum / (case + 1))
                testAgent.clearState()
                print(case, result[-1], " | ", int(average[-1]))
                break
    with open("rawData.json", "w") as f:
        json.dump(result, f)
    with open("average.json", "w") as f:
        json.dump(average, f)
