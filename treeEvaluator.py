import os
import time
from typing import Optional, List
from emulator.emulator_core import GameOverException, move, random_tile_generate
from emulator.emulator_api import check_state, tree_evaluation, get_empty_tile
from emulator.terminal_interface import render_board

def evaluate(state): return len(get_empty_tile(state))
def average(iterator): return sum(iterator) / len(iterator)

class treeEvaluateAgent:
    """
    Describe your Agent
    """
    def __init__(self, initialState: Optional[List[List]]=None) -> None:
        self.state = initialState if initialState is not None else \
            random_tile_generate([[0] * 4 for _ in range(4)])
        self.stepCount = 0
        ########## INITIALIZE HERE ############

        #######################################

    def make_move(self, withGUI=True):
        startTime = time.time()
        ########### WRITE CODE BELOW ##########
        if not check_state(self.state): raise GameOverException()
        scores = tree_evaluation(self.state,
            evaluate,
            average,
            useMultiProcess=True,
            # depth = max(3, 6 - len(get_empty_tile(self.state))),
            depth = 6,
            random=(True, 3)
        )
        action, maxScore = "left", -1000
        for a in scores:
            if scores[a] > maxScore:
                action = a
                maxScore = scores[a]
        self.state, isValid = move(self.state, action)
        #######################################
        endTime = time.time()
        self.stepCount += 1
        print("STEP {}".format(self.stepCount))
        print("Process time: {}s".format(endTime - startTime))
        render_board(self.state)

if __name__ == "__main__":
    print("Working on directory: ", os.getcwd())
    testAgent = treeEvaluateAgent()
    while True:
        testAgent.make_move()
