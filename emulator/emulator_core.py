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
    # Compress action
    if direction == "up":
        for col in range(0, len(gameState[0]), 1):
            fullCol = [gameState[_][col] for _ in range(0, len(gameState), 1) if gameState[_][col] != 0]
            for idx, item in enumerate(fullCol): newState[idx][col] = item
    elif direction == "down":
        for col in range(0, len(gameState[0]), 1):
            fullCol = [gameState[_][col] for _ in range(len(gameState) - 1, -1, -1) if gameState[_][col] != 0]
            for idx, item in enumerate(fullCol): newState[len(gameState) - 1 - idx][col] = item
    elif direction == "left":
        for row in range(0, len(gameState), 1):
            fullRow = [gameState[row][_] for _ in range(0, len(gameState[0]), 1) if gameState[row][_] != 0]
            for idx, item in enumerate(fullRow): newState[row][idx] = item
    else:
        for row in range(0, len(gameState), 1):
            fullRow = [gameState[row][_] for _ in range(len(gameState[0]) - 1, -1, -1) if gameState[row][_] != 0]
            for idx, item in enumerate(fullRow): newState[row][len(gameState[0]) - 1 - idx] = item
    # is updated
    isValid = False
    for row in range(len(gameState)):
        for col in range(len(gameState[0])):
            isValid = isValid or gameState[row][col] != newState[row][col]
    
    return newState, isValid


def merge(gameState:List[List], direction: str) -> Tuple[List[List], bool]:
    assert direction in {"up", "down", "left", "right"}, "Expect direction to be 'left', 'right', 'up' or 'down', get: {}".format(direction)
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
            elif gameState[row + dx][col + dy] == gameState[row][col] and gameState[row][col] != 0:
                newState[row + dx][col + dy] = gameState[row][col] * 2
                gameState[row][col] = 0
                gameState[row + dx][col + dy] = 0
                isChanged = True
    for row in range(len(gameState)):
        for col in range(len(gameState[0])):
            if gameState[row][col] != 0: newState[row][col] = gameState[row][col]
    return newState, isChanged

def random_tile_generate(gameState: List[List]) -> List[List]:
    if any(0 in row for row in gameState):
        row, col = random.randint(0, len(gameState) - 1), random.randint(0, len(gameState[0]) - 1)
        while gameState[row][col] != 0:
            row, col = random.randint(0, len(gameState) - 1), random.randint(0, len(gameState[0]) - 1)
        gameState[row][col] = random.randint(1, 2) * 2
        return gameState
    else:
        return gameState

class GameOverException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)