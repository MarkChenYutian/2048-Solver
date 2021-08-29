from typing import List
from emulator_core import move
from typing import List, Tuple

def get_valid_actions(gameState: List[List]) -> List[Tuple[str, List[List]]]:
    originalGameState = [[elem for elem in row] for row in gameState]
    nextState = []
    for action in ["left", "right", "up", "down"]:
        gameState = [[elem for elem in row] for row in originalGameState]
        nextState, isValid = move(gameState, action)
        if isValid: nextState.append((action, nextState))
    return nextState
