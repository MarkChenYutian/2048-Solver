import time

from abc import ABC, abstractmethod
from typing import Optional, List

from emulator.emulator_core import GameOverException, random_tile_generate, move
from emulator.terminal_interface import render_board

class Agent(ABC):
    def __init__(self, initialState: Optional[List[List]]=None) -> None:
        self.state = initialState if initialState is not None else \
            random_tile_generate([[0] * 4 for _ in range(4)])
        self.stepCount = 0
    
    def make_move(self, withGUI=True) -> None:
        startTime = time.time()
        pendingAction = self.make_decision()
        assert pendingAction in {"up", "left", "down", "right"}, f"make_decition function should return \
            either 'up', 'left', 'down' or 'right', instead, the function returns {pendingAction}"
        self.state, isValid = move(self.state, pendingAction)
        if not isValid: raise GameOverException
        endTime = time.time()
        self.stepCount += 1
        if withGUI:
            print("STEP {}".format(self.stepCount))
            print("Process time: {}s".format(endTime - startTime))
            render_board(self.state)
    
    @abstractmethod
    def make_decision(self) -> str:
        """
        evaluate and return an action ("up", "down", "left", "right")
        this method is called by make_move() function.
        """
    
    def clearState(self) -> None:
        """
        Reset the agent state to initial state
        """
        self.state = random_tile_generate([[0] * 4 for _ in range(4)])
        self.stepCount = 0
