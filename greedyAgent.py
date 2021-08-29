import os
import time
from typing import Optional, List
from emulator.emulator_core import move, random_tile_generate
from emulator.emulator_api import get_valid_actions, get_empty_tile
from emulator.terminal_interface import render_board


class GreedyAgent:
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

        maxEmpty, pendingAction = 0, ""
        for action in validActions:
            if len(get_empty_tile(validActions[action])) > maxEmpty:
                pendingAction = action
                maxEmpty = len(get_empty_tile(validActions[action]))
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
    testAgent = GreedyAgent()
    while True:
        testAgent.make_move()
