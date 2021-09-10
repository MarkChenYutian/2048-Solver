from typing import Optional, List

from emulator.emulator_core import GameOverException
from emulator.emulator_api import get_valid_actions, get_empty_tile
from emulator.agent import Agent


class GreedyAgent(Agent):
    """
    A greedy agent that wants to maximize the amount of empty tile on board
    """
    def __init__(self, initialState: Optional[List[List]]=None) -> None:
        super().__init__(initialState=initialState)

    def make_decision(self) -> str:
        validActions = get_valid_actions(self.state)
        # Select the action that leads to maximum amount of empty tiles
        maxEmpty, pendingAction = 0, ""
        for action in validActions:
            if len(get_empty_tile(validActions[action])) > maxEmpty:
                pendingAction = action
                maxEmpty = len(get_empty_tile(validActions[action]))
        if len(validActions) == 0 or pendingAction == "": raise GameOverException()
        return pendingAction
