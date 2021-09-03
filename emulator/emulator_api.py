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
    """
    Get the empty tiles in gameState, return a list of (row, col) of empty tiles
    """
    emptySpace = []
    for row in range(len(gameState)):
        for col in range(len(gameState[0])):
            if gameState[row][col] == 0: emptySpace.append((row, col))
    return emptySpace

def check_state(gameState: List[List]) -> bool:
    '''
    Check the state of the game.
    If a further move is possible, return True. Otherwise, False.
    '''
    # Specify dimension
    r, c = len(gameState), len(gameState[0])
    # Check empty space
    if any(0 in row for row in gameState):
        return True
    # Check possible merge cases (main region)
    for i in range(r - 1):
        for j in range(c - 1):
            if (gameState[i][j] == gameState[i + 1][j]) or (gameState[i][j] == gameState[i][j + 1]):
                return True
    # Check possible merge cases (last row)
    for j in range(c - 1):
        if gameState[r - 1][j] == gameState[r - 1][j + 1]:
            return True
    # Check possible merge cases (last column)
    for i in range(r - 1):
        if gameState[i][c - 1] == gameState[i + 1][c - 1]:
            return True
    return False

def get_max_tile(gameState:List[List]) -> Tuple[int, Tuple[int, int]]:
    """
    Given a game state, return the value and position of max tile.
    """
    row, col, value = -1, -1, -1
    for r in gameState:
        for c, item in enumerate(r):
            if item > value:
                value, row, col = item, r, c
    return (value, (row, col))
