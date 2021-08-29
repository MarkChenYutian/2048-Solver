import unittest
from emulator_core import pure_move

class EmulatorTest(unittest.TestCase):
    def test_upper(self):
        state1 = [
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        