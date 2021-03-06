"""
This file describe the FEATURE EXTRACT FUNCTION(s), not the emulator itself.
"""
import multiprocessing as mp
from emulator.emulator_core import GameOverException, pure_move, random_tile_generate
from typing import Dict, List, Tuple
from copy import deepcopy

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

def count_merge_case(gameState: List[List]) -> int:
    """
    Count the number of possible merge cases in gameState
    """
    count = 0
    # Specify dimension
    r, c = len(gameState), len(gameState[0])
    # Check possible merge cases (main region)
    for i in range(r - 1):
        for j in range(c - 1):
            if (gameState[i][j] == gameState[i + 1][j]) or (gameState[i][j] == gameState[i][j + 1]):
                count += 1
    # Check possible merge cases (last row)
    for j in range(c - 1):
        if gameState[r - 1][j] == gameState[r - 1][j + 1]:
            count += 1
    # Check possible merge cases (last column)
    for i in range(r - 1):
        if gameState[i][c - 1] == gameState[i + 1][c - 1]:
            count += 1
    # Check possible merge cases in each row that are not adjacent to one another:
    for row in gameState:
        row = list(filter((0).__ne__, row))
        for i in range(len(row) - 1):
            if row[i] == row[i + 1]:
                count += 1
    # Check possible merge cases in each column that are not adjacent to one another
    for j in range(c):
        col = [row[j] for row in gameState]
        col = list(filter((0).__ne__, col))
        for k in range(len(col) - 1):
            if col[k] == col[k + 1]:
                count += 1
    return count

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

def tree_evaluation(
        state: List[List],
        evaluate_fn,
        comb_fn,
        depth: int,
        sampling: Tuple[bool, int] = (False, 0),
        useMultiProcess: bool = False,
        gameOverScore: float = 0):
    """
    :param state: Current State you want to evaluate each action on
    :param evaluate_fn: The function to evaluate each state
    :param comb_fn: The function to combine all possible states after each action (usally average / min / max)
    :param depth: The depth of tree_evaluate
    :param random: A tuple, if the 0th item is True, then 1st item represent the number of random_tile generation applied
    on the current state to evaluate.
    :param gameOverScore: the score to return when a game is at terminal state
    """
    scores = {a: 0 for a in ["up", "left", "down", "right"]}
    if not check_state(state): return scores
    validActions = get_valid_actions(state)
    if useMultiProcess:
        actionList = list(validActions.keys())
        with mp.Pool(len(actionList)) as p:
            score_list = p.map(func=tree_evaluation_subProcess,
                iterable=[(state, validActions[a], evaluate_fn, comb_fn, depth - 1, sampling, gameOverScore) for a in actionList])
            for i, action in enumerate(actionList):
                scores[action] = score_list[i]
    else:
        for action in validActions:
            if sampling[0]:
                possibleStates = [random_tile_generate(validActions[action]) for _ in range(sampling[1])]
            else:
                empty_space = get_empty_tile(state)
                possibleStates = []
                for x, y in empty_space:
                    next_state = deepcopy(validActions[action])
                    next_state[x][y] = 2
                    possibleStates.append(next_state)
                for x, y in empty_space:
                    next_state = deepcopy(validActions[action])
                    next_state[x][y] = 4
                    possibleStates.append(next_state)
            if depth == 1:
                scores[action] = comb_fn([evaluate_fn(ns) + 0.5 for ns in possibleStates])
            else:
                scores[action] = comb_fn([max(tree_evaluation(ns, 
                    evaluate_fn, 
                    comb_fn, 
                    depth - 1, 
                    sampling=sampling, 
                    gameOverScore=gameOverScore).values()) for ns in possibleStates])
    return scores

def tree_evaluation_subProcess(args):
    state, ns, evaluate_fn, comb_fn, depth, sampling, gameOverScore = args
    if sampling[0]:
        possibleStates = [random_tile_generate(ns) for _ in range(sampling[1])]
    else:
        empty_space = get_empty_tile(state)
        possibleStates = []
        for x, y in empty_space:
            next_state = deepcopy(ns)
            next_state[x][y] = 2
            possibleStates.append(next_state)
        for x, y in empty_space:
            next_state = deepcopy(ns)
            next_state[x][y] = 4
            possibleStates.append(next_state)
    if depth == 1:
        return comb_fn([evaluate_fn(ns) + 0.5 for ns in possibleStates])
    else:
        return comb_fn([max(tree_evaluation(ns, 
            evaluate_fn, 
            comb_fn, 
            depth - 1, 
            sampling=sampling, 
            gameOverScore=gameOverScore).values()) for ns in possibleStates])
        
def get_new_max(gameState_0: List[List], gameState_1: List[List]) -> int:
    """
    Given to gameStates, return the newly-generated maximum number
    """
    max_num = 0
    for row in range(len(gameState_0)):
        for col in range(len(gameState_0[0])):
            if gameState_0[row][col] != gameState_1[row][col] \
                and gameState_1[row][col] > max_num\
                and gameState_0[row][col] != 0:
                max_num = gameState_1[row][col]
    return max_num
