import os
import time
import uuid
import json
import random
from typing import Optional, List, Dict
from emulator.emulator_core import move, random_tile_generate, GameOverException
from emulator.emulator_api import get_valid_actions, get_empty_tile, get_max_tile, check_state
from emulator.terminal_interface import render_board


class GeneticAlgorithmAgent:
    """
    Genetic Algorithm Agent use GA to optimize its operation.
    """

    def __init__(self,
                 fromAgent: List[str],
                 paramDict: Optional[Dict] = None,
                 initialState: Optional[List[List]] = None) -> None:

        self.state = initialState if initialState is not None else \
            random_tile_generate([[0] * 4 for _ in range(4)])
        self.stepCount = 0
        ########## INITIALIZE HERE ############
        self.id = str(uuid.uuid4())
        self.from_id = fromAgent
        self.parameter = {
            "empty_tile_weight": random.random(),   # The weight on empty tile number
            "max_tile_weight": random.random(),     # The weight on maximum tile in resulted case
            # Preference on each action
            "up_preference": random.random(),       
            "down_preference": random.random(),
            "left_preference": random.random(),
            "right_preference": random.random()
        } if paramDict is None else paramDict
        #######################################

    def make_move(self, withGUI=True):
        startTime = time.time()
        ########### WRITE CODE BELOW ##########
        actionScore = {key: 0 for key in ["up", "down", "left", "right"]}
        validActions = get_valid_actions(self.state)

        if not check_state(self.state): raise GameOverException()

        # Evaluate each action
        for action in validActions:
            nextState = validActions[action]
            actionScore[action] = len(get_empty_tile(nextState)) * self.parameter["empty_tile_weight"] + \
                                  get_max_tile(nextState)[0] * self.parameter["max_tile_weight"] + \
                                  self.parameter[action + "_preference"]

        # Select action based on evaluation
        max_score, pendingAction = -1 * float("inf"), ""
        for action in actionScore:
            if actionScore[action] > max_score:
                max_score = actionScore[action]
                pendingAction = action

        if len(validActions) == 0 or pendingAction == "" : raise GameOverException()

        self.state, isValid = move(self.state, pendingAction)
        #######################################
        endTime = time.time()
        self.stepCount += 1
        if withGUI:
            print("STEP {}".format(self.stepCount))
            print("Process time: {}s".format(endTime - startTime))
            render_board(self.state)

    def hybrid(self, o: 'GeneticAlgorithmAgent') -> List['GeneticAlgorithmAgent']:
        """
        Hybrid two Agents to get Next Generation.
        """
        results = []
        for i in range(4):
            results.append(
                GeneticAlgorithmAgent([self.id, o.id], {
                    key :random.choice([self.parameter[key], o.parameter[key]]) for key in self.parameter
                })
            )
        return results

    def mutate(self) -> 'GeneticAlgorithmAgent':
        """
        Mutate the parameter of agent to add diversity
        """
        return GeneticAlgorithmAgent([self.id], paramDict={
            "empty_tile_weight" : self.parameter["empty_tile_weight"] + random.random() * random.choice([0.25, -0.25]),
            "max_tile_weight"   : self.parameter["max_tile_weight"] + random.random() * random.choice([0.25, -0.25]),
            "up_preference"     : self.parameter["up_preference"] + random.random() * random.choice([0.25, -0.25]),
            "down_preference"   : self.parameter["down_preference"] + random.random() * random.choice([0.25, -0.25]),
            "left_preference"   : self.parameter["left_preference"] + random.random() * random.choice([0.25, -0.25]),
            "right_preference"  : self.parameter["right_preference"] + random.random() * random.choice([0.25, -0.25]),
        })

    def clearState(self) -> None:
        """
        Reset the agent state to initial state (randomized)
        """
        self.state = random_tile_generate([[0] * 4 for _ in range(4)])

    def dump(self, fileName, score) -> None:
        with open("./storage/GeneticAlgorithm/{}.json".format(self.id if fileName is None else fileName), "w") as f:
            json.dump({
                "parameter": self.parameter,
                "id": self.id,
                "from": self.from_id,
                "finalState": self.state,
                "score": score
            }, f, indent=4)

    def evaluate(self, numTest=8) -> int:
        """
        Return the average step in numTest (default 10) tests
        """
        scores = []
        for i in range(numTest):
            scores.append(0)
            self.clearState()
            while True:
                try:
                    self.make_move(withGUI=False)
                    scores[-1] += 1
                except GameOverException:
                    #scores[-1] = (scores[-1] * 00.1) * get_max_tile(self.state)[0]
                    scores[-1] = get_max_tile(self.state)[0]
                    break
        return sum(scores) / len(scores)


class GeneticAlgorithmTrainer:
    def __init__(self, firstRoundNum=14):
        self.round = 0
        self.world = [[0, GeneticAlgorithmAgent([''])] for _ in range(firstRoundNum)]

    def assessmentGeneration(self):
        print("正在高速内卷中 ^_^", end="", flush=True)
        for i in range(len(self.world)):
            self.world[i][0] = self.world[i][1].evaluate()
        print("\r内卷完毕，本轮结果：")
        print([item[0] for item in self.world],
              "Avg: {}".format(sum([item[0] for item in self.world]) / len(self.world)),
              "Max: {}".format(max([item[0] for item in self.world]))
              )

    def createNextGeneration(self):
        nextGen = []
        # 选出来卷王两位
        self.world.sort(key=lambda item: item[0], reverse=True)
        agent_1, agent_2 = self.world[0], self.world[1]
        agent_1[1].dump("Round {}".format(self.round), agent_1[0])
        # 两位卷王直接进入下一轮
        nextGen += [agent_1[1], agent_2[1]]
        # 杂交两位卷王
        nextGen += agent_1[1].hybrid(agent_2[1])
        # 让两位卷王的杂交后代突变一次，引入变化量
        nextGen += [agent.mutate() for agent in agent_1[1].hybrid(agent_2[1])]
        # 随机选 n-10 位卢瑟进行突变，增加 gene diversity
        nextGen += [
            self.world[random.randint(2, len(self.world) - 1)][1].mutate()
            for _ in range(len(self.world) - 10)
        ]
        self.world = [[0, agent] for agent in nextGen]
        self.round += 1


if __name__ == "__main__":
    print("Working on directory: ", os.getcwd())
    trainer = GeneticAlgorithmTrainer()
    while True:
        trainer.assessmentGeneration()
        trainer.createNextGeneration()
