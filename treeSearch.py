import time
from typing import Optional, List
from emulator.emulator_api import get_valid_actions, get_empty_tile, check_state
from emulator.emulator_core import random_tile_generate, GameOverException, move
from emulator.terminal_interface import render_board


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children = []

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_level(self):
        level = 0
        parent = self.parent
        while parent:
            parent = parent.parent
            level += 1
        return level

    def print_tree(self):
        prefix = "\t" * self.get_level() + "|___" if self.parent else ""
        print(prefix + str(self.data[0]))
        for child in self.children:
            child.print_tree()


class MaxEmptyAgent:
    """
    An agent to search for the action maximizing empty tiles within 3 steps
    """
    def __init__(self, initialState: Optional[List[List]] = None) -> None:
        self.state = initialState if initialState else \
            random_tile_generate([[0] * 4 for _ in range(4)])
        self.stepCount = 0

    def make_move(self):
        # start timing
        sTime = time.time()

        # create the root of a tree
        root = TreeNode(("root", self.state))

        # count, in the end, the amount of empty tiles of each action
        emptyCount = dict()

        vAction = get_valid_actions(self.state)
        if not check_state(self.state): raise GameOverException
        for action, state in vAction.items():
            emptyCount[action] = 0
            for _ in range(len(get_empty_tile(state)) * 2):
                root.add_child(TreeNode((action, random_tile_generate(state))))
                emptyCount[action] += len(get_empty_tile(state))

        for child0 in root.children:
            vAction = get_valid_actions(child0.data[1])
            if not check_state(self.state): raise GameOverException
            for action, state in vAction.items():
                for _ in range(len(get_empty_tile(state)) * 2):
                    child0.add_child(TreeNode((action, random_tile_generate(state))))
                    emptyCount[child0.data[0]] += len(get_empty_tile(state))

        for child0 in root.children:
            for child1 in child0.children:
                vAction = get_valid_actions(child1.data[1])
                if not check_state(self.state): raise GameOverException
                for action, state in vAction.items():
                    for _ in range(len(get_empty_tile(state)) * 2):
                        child1.add_child(TreeNode((action, random_tile_generate(state))))
                        emptyCount[child0.data[0]] += len(get_empty_tile(state))

        for child0 in root.children:
            for child1 in child0.children:
                for child2 in child1.children:
                    vAction = get_valid_actions(child2.data[1])
                    if not check_state(self.state): raise GameOverException
                    for action, state in vAction.items():
                        for _ in range(len(get_empty_tile(state)) * 2):
                            child2.add_child(TreeNode((action, random_tile_generate(state))))
                            emptyCount[child0.data[0]] += len(get_empty_tile(state))

        # execute action with maximum number of empty tiles
        emptyCount = {key: value for key, value in sorted(emptyCount.items(), key=lambda item: item[1], reverse=True)}
        self.state, isValid = move(self.state, tuple(emptyCount)[0])
        self.stepCount += 1

        # end timing
        eTime = time.time()

        # display necessary info
        # root.print_tree()
        print("-" * 65)
        print(f"STEP {self.stepCount}")
        print(f"Process Time: {eTime - sTime}s")
        print(emptyCount)
        print("-" * 65)
        render_board(self.state)


if __name__ == "__main__":
    testAgent = MaxEmptyAgent()
    while True:
        testAgent.make_move()
