import uuid
import json
import random
import multiprocessing as mp

from typing import Optional, List, Dict

from emulator.emulator_core import GameOverException
from emulator.emulator_api import get_valid_actions, get_empty_tile, check_state, get_max_tile
from emulator.agent import Agent


class GeneticAlgorithmAgent(Agent):
    """
    Genetic Algorithm Agent use GA to optimize its operation.
    """

    def __init__(self,
                 fromAgent: List[str],
                 paramDict: Optional[Dict] = None,
                 initialState: Optional[List[List]] = None) -> None:
        super().__init__(initialState=initialState)
        ########## INITIALIZE HERE ############
        self.id = str(uuid.uuid4())
        self.from_id = fromAgent
        self.score = 0
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
    def make_decision(self) -> str:
        actionScore = {key: 0 for key in ["up", "down", "left", "right"]}
        validActions = get_valid_actions(self.state)

        if not check_state(self.state): raise GameOverException()

        # Evaluate each action
        for action in validActions:
            nextState = validActions[action]
            # get_new_max(self.state, nextState) * self.parameter["max_tile_weight"] + \
            actionScore[action] = len(get_empty_tile(nextState)) * self.parameter["empty_tile_weight"] + \
                                    get_max_tile(nextState)[0] * self.parameter["max_tile_weight"] + \
                                    self.parameter[action + "_preference"]

        # Select action based on evaluation
        max_score, pendingAction = -1000, ""
        for action in actionScore:
            if actionScore[action] > max_score:
                max_score = actionScore[action]
                pendingAction = action

        if len(validActions) == 0 or pendingAction == "" : raise GameOverException()

        return pendingAction

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
            "empty_tile_weight" : self.parameter["empty_tile_weight"] + random.random() * random.choice([0.1, -0.1]),
            "max_tile_weight"   : self.parameter["max_tile_weight"] + random.random() * random.choice([0.1, -0.1]),
            "up_preference"     : self.parameter["up_preference"] + random.random() * random.choice([0.1, -0.1]),
            "down_preference"   : self.parameter["down_preference"] + random.random() * random.choice([0.1, -0.1]),
            "left_preference"   : self.parameter["left_preference"] + random.random() * random.choice([0.1, -0.1]),
            "right_preference"  : self.parameter["right_preference"] + random.random() * random.choice([0.1, -0.1]),
        })

    def dump(self, fileName, score) -> None:
        with open("./storage/GeneticAlgorithm/{}.json".format(self.id if fileName is None else fileName), "w") as f:
            json.dump({
                "parameter": self.parameter,
                "id": self.id,
                "from": self.from_id,
                "finalState": self.state,
                "score": score
            }, f, indent=4)

    def evaluate(self, numTest=100) -> int:
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

def wrapper(obj): return obj.evaluate()

class GeneticAlgorithmTrainer:
    def __init__(self, firstRoundNum=14):
        self.round = 0
        self.world = [[0, GeneticAlgorithmAgent([''])] for _ in range(firstRoundNum)]
        self.max_sequence = []

    def assessmentGeneration(self):
        print("????????????????????? ^_^", end="", flush=True)
        
        with mp.Pool(len(self.world)) as p:
            scores = p.map(func=wrapper, iterable=[self.world[_][1] for _ in range(len(self.world))])

        for i in range(len(self.world)):
            self.world[i][0]  = scores[i]
        print("\r??????????????????????????????")
        print([item[0] for item in self.world],
              "Avg: {}".format(sum([item[0] for item in self.world]) / len(self.world)),
              "Max: {}".format(max([item[0] for item in self.world]))
              )
        self.max_sequence.append(max([item[0] for item in self.world]))

    def createNextGeneration(self):
        nextGen = []
        # ?????????????????????
        self.world.sort(key=lambda item: item[0], reverse=True)
        agent_1, agent_2 = self.world[0], self.world[1]
        agent_1[1].dump("Round {}".format(self.round), agent_1[0])
        # ?????????????????????????????????
        nextGen += [agent_1[1], agent_2[1]]
        # ??????????????????
        nextGen += agent_1[1].hybrid(agent_2[1])
        # ????????????????????????????????????????????????????????????
        nextGen += [agent.mutate() for agent in agent_1[1].hybrid(agent_2[1])]
        # ????????? n-10 ?????????????????????????????? gene diversity
        nextGen += [
            self.world[random.randint(2, len(self.world) - 1)][1].mutate()
            for _ in range(len(self.world) - 10)
        ]
        self.world = [[0, agent] for agent in nextGen]
        self.round += 1
