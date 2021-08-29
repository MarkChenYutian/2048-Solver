"""
By Mark, 2021 Aug 28th, emulator_core.py
This file defines the 2048 emulator core.
"""

import random
from typing import List, Tuple

def move(gameState: List[List], direction: str) -> Tuple[List[List], bool]:
    """
    Move gamestate towards specific direction
    Return True as second value if it is a valid move, False otherwise
    """
    gameState, isValid = pure_move(gameState, direction)
    if isValid:
        return random_tile_generate(gameState), True
    else:
        return gameState, False

def pure_move(gameState: List[List], direction: str) -> Tuple[List[List], bool]:
    """
    Only move the state, not adding random tiles (Do not call this function, call move() instead.)
    """
    gameState, change_1 = compress(gameState, direction)
    gameState, change_2 = merge(gameState, direction)
    gameState, change_3 = compress(gameState, direction)
    return gameState, (change_1 or change_2 or change_3)

def compress(gameState: List[List], direction: str) -> Tuple[List[List], bool]:
    assert direction in {"up", "down", "left", "right"}, "Expect direction to be 'left', 'right', 'up' or 'down', get: {}".format(direction)
    newState = [[0] * len(gameState[0]) for _ in range(len(gameState))]
    isChanged = False
    i_initial, i_delta = {
            "up": (0, 1),
            "down": (len(gameState) - 1, -1),
            "left": (0, 1),
            "right": (len(gameState[0]) - 1, -1)
        }[direction]
    if direction in ["up", "down"]:   
        for x in range(len(gameState[0])):
            i = i_initial
            for y in range(len(gameState)):
                if gameState[y][x] != 0:
                    newState[i][x] = gameState[y][x]
                    i += i_delta
                    isChanged = True
    elif direction in ["left", "right"]:
        for x in range(len(gameState)):
            i = i_initial
            for y in range(len(gameState[0])):
                if gameState[x][y] != 0:
                    newState[x][i] = gameState[x][y]
                    i += i_delta
                    isChanged = True
    return newState, isChanged


def merge(gameState:List[List], direction: str) -> Tuple[List[List], bool]:
    assert direction in {"up", "down", "left", "right"}, "Expect direction to be 'left', 'right', 'up' or 'down'"
    dx, dy = {
        "up": (1, 0),
        "down": (-1, 0),
        "left": (0, -1),
        "right": (0, 1) 
    }[direction]
    newState = [[0] * len(gameState[0]) for _ in range(len(gameState))]
    isChanged = False

    for row in range(len(gameState)):
        for col in range(len(gameState[0])):
            if not(-1 < row + dx < len(gameState) and -1 < col + dy < len(gameState[0])):
                continue
            elif gameState[row + dx][col + dy] == gameState[row][col]:
                newState[row + dx][col + dy] = gameState[row][col] * 2
                gameState[row][col] = 0
                gameState[row + dx][col + dy] = 0
                isChanged = True
    for row in range(len(gameState)):
        for col in range(len(gameState[0])):
            if gameState[row][col] != 0: newState[row][col] = gameState[row][col]
    return newState, isChanged

def random_tile_generate(gameState) -> List[List]:
    row, col = random.randint(0, len(gameState) - 1), random.randint(0, len(gameState[0]) - 1)
    while gameState[row][col] != 0:
        row, col = random.randint(0, len(gameState) - 1), random.randint(0, len(gameState[0]) - 1)
    gameState[row][col] = random.randint(1, 2) * 2
    return gameState

