from typing import Optional, List

from emulator.emulator_core import GameOverException
from emulator.emulator_api import check_state, tree_evaluation, get_empty_tile
from emulator.agent import Agent

def evaluate(state): return len(get_empty_tile(state))
def average(iterator): return sum(iterator) / len(iterator)

class TreeEvaluateAgent(Agent):
    def __init__(self, initialState: Optional[List[List]]=None) -> None:
        super().__init__(initialState=initialState)
    
    def make_decision(self) -> str:
        if not check_state(self.state): raise GameOverException()
        scores = tree_evaluation(self.state,
            evaluate,
            average,
            useMultiProcess=True,
            depth = max(4, 7 - len(get_empty_tile(self.state))),
            sampling=(True, 3)
        )
        action, maxScore = "left", -1000
        for a in scores:
            if scores[a] > maxScore:
                action = a
                maxScore = scores[a]
        return action

