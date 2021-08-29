from emulator_core import move
from terminal_interface import render_board

if __name__ == "__main__":
    gameState = [
        [0, 0, 0, 0],
        [0, 0, 2, 0],
        [0, 0, 0, 4],
        [0, 0, 64, 4]
    ]
    render_board(gameState)
    gameState, isValid = move(gameState, "down")
    render_board(gameState)
