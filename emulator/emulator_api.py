from emulator.emulator_core import pure_move
from typing import Dict, List, Tuple

def get_valid_actions(gameState: List[List]) -> Dict[str, List[List]]:
    """
    Return a dictionary in structure { direction: gameState }
    NOTICE: The newGameState is the result of move and has no random tile generated.

    Example:
    >>> from emulator_core import random_tile_generate

    >>> validActions = get_valid_actions(currentState)
    >>> # Do what ever to choose an action between all valid actions
    >>> newState = random_tile_generate(validActions[chosenAction]) # Ok
    Or
    >>> newState = move(currentState, chosenAction)     #Ok
    But this is not Ok:
    >>> newState = validActions[chosenAction]   # ERROR!
    """
    originalGameState = [[elem for elem in row] for row in gameState]
    nextStates = dict()
    for action in ["left", "right", "up", "down"]:
        gameState = [[elem for elem in row] for row in originalGameState]
        nextState, isValid = pure_move(gameState, action)
        if isValid: nextStates[action] = nextState
    return nextStates

def get_empty_tile(gameState) -> List[Tuple[int, int]]:
    emptySpace = []
    for row in range(len(gameState)):
        for col in range(len(gameState[0])):
            if gameState[row][col] == 0: emptySpace.append((row, col))
    return emptySpace

if __name__ == "__main__":
    print("import Ok.")