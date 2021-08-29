"""
By Mark, 2021 Aug 28th
This file define the gui interface of emulator. With GUI, you can debug easier in terminal.
"""

from typing import List


def render_board(state: List[List]) -> None:
    print("")
    max_value_digits = len(str(max([max(row) for row in state])))
    for row in range(len(state)):
        for col in range(len(state[0])):
            if state[row][col]!= 0:
                print(str(state[row][col]).ljust(max_value_digits)+ " | ", end="")
            else:
                print(".".ljust(max_value_digits) + " | ", end="")
        print("")
