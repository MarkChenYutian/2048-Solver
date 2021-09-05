import os
import time
import json
from typing import Optional, List
from emulator.emulator_core import GameOverException, move, random_tile_generate
from emulator.emulator_api import get_valid_actions, get_empty_tile, get_max_tile
from emulator.terminal_interface import render_board


class GreedyAgent:
    """
    A greedy agent that wants to maximize the amount of empty tile on board
    """
    def __init__(self, initialState: Optional[List[List]]=None) -> None:
        self.state = initialState if initialState is not None else \
            random_tile_generate([[0] * 4 for _ in range(4)])
        self.stepCount = 0

    def make_move(self, withGUI=True):
        startTime = time.time()
        validActions = get_valid_actions(self.state)

        # Select the action that leads to maximum amount of empty tiles
        maxEmpty, pendingAction = 0, ""
        for action in validActions:
            if len(get_empty_tile(validActions[action])) > maxEmpty:
                pendingAction = action
                maxEmpty = len(get_empty_tile(validActions[action]))
        
        if len(validActions) == 0 or pendingAction == "": raise GameOverException()

        self.state, isValid = move(self.state, pendingAction)
        endTime = time.time()
        self.stepCount += 1
        if withGUI:
            print("STEP {}".format(self.stepCount))
            print("Process time: {}s".format(endTime - startTime))
            render_board(self.state)
    
    def clearState(self) -> None:
        """
        Reset the agent state to initial state (randomized)
        """
        self.state = random_tile_generate([[0] * 4 for _ in range(4)])
        self.stepCount = 0

if __name__ == "__main__":
    print("Working on directory: ", os.getcwd())
    testAgent = GreedyAgent()
    result = []
    average = []
    curr_sum = 0
    for case in range(2000):
        while True:
            try:
                testAgent.make_move(withGUI=False)
            except GameOverException:
                score = get_max_tile(testAgent.state)[0]
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


