import os
import time
from typing import Optional, List
from emulator.emulator_core import move, random_tile_generate
from emulator.emulator_api import get_valid_actions
from emulator.terminal_interface import render_board


class GreedyScoreAgent:
    """
    A greedy agent that wants to maximize the amount of empty tile on board
    """
    def __init__(self, initialState: Optional[List[List]]=None) -> None:
        self.state = initialState if initialState is not None else \
            random_tile_generate([[0] * 4 for _ in range(4)])
        self.stepCount = 0

    def make_move(self):
        startTime = time.time()
        validActions = get_valid_actions(self.state)

        max_tile, pendingAction = max([max(row) for row in self.state]), list(validActions.keys())[0]
        for action in validActions:
            next_max = max([max(row) for row in validActions[action]])
            if next_max > max_tile:
                max_tile = next_max
                pendingAction = action

        if len(validActions) == 0 or pendingAction == "":
            print("Game Over. GG")
            raise Exception("Game Over")

        self.state, isValid = move(self.state, pendingAction)

        endTime = time.time()
        self.stepCount += 1
        print("STEP {}".format(self.stepCount))
        print("Process time: {}s".format(endTime - startTime))
        render_board(self.state)

if __name__ == "__main__":
    print("Working on directory: ", os.getcwd())
    testAgent = GreedyScoreAgent()
    while True:
        testAgent.make_move()
