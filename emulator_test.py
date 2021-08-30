import unittest
from emulator.emulator_core import random_tile_generate, pure_move
from emulator.emulator_api import check_state


class EmulatorTest(unittest.TestCase):
    def test_check_state(self):
        actual = check_state(
            [[2, 4, 8, 16],
             [32, 64, 128, 256]]
        )
        self.assertEqual(actual, False)

        actual = check_state(
            [[2, 4, 8],
             [8, 16, 2],
             [2, 4, 2]]
        )
        self.assertEqual(actual, True)

        actual = check_state(
            [[16, 8, 4],
             [8, 2, 8],
             [4, 4, 2]]
        )
        self.assertEqual(actual, True)

    def test_random_tile_generate(self):
        actual = random_tile_generate(
            [[2, 4, 8],
             [8, 16, 2],
             [2, 4, 2]]
        )
        expected = [[2, 4, 8],
                    [8, 16, 2],
                    [2, 4, 2]]
        self.assertEqual(actual, expected)

        actual = any(2 or 4 in row for row in
                     random_tile_generate(
                         [[0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]]
                     ))
        expected = True
        self.assertEqual(actual, expected)

        actual = any(2 or 4 in row for row in
                     random_tile_generate(
                         [[8, 8, 8, 8],
                          [8, 8, 8, 8],
                          [8, 0, 8, 8],
                          [8, 8, 8, 8]]
                     ))
        expected = True
        self.assertEqual(actual, expected)

    def test_pure_move(self):
        actual = pure_move(
            [[0, 2, 0, 2],
             [2, 2, 2, 0],
             [0, 0, 0, 2],
             [2, 0, 0, 2]], "left"
        )
        expected = [
                       [4, 0, 0, 0],
                       [4, 2, 0, 0],
                       [2, 0, 0, 0],
                       [4, 0, 0, 0]
                   ], True
        self.assertEqual(actual, expected)

        actual = pure_move(
             [[0, 2, 8, 2],
             [2, 4, 2, 4],
             [0, 0, 0, 2],
             [2, 4, 8, 2]], "right"
        )
        expected = [
                       [0, 2, 8, 2],
                       [2, 4, 2, 4],
                       [0, 0, 0, 2],
                       [2, 4, 8, 2]
                   ], False
        self.assertEqual(actual, expected)

        actual = pure_move([[0, 2, 4, 2],
                            [0, 0, 2, 2],
                            [0, 0, 0, 2],
                            [2, 8, 4, 2]], "up"
                           )
        expected = [[2, 2, 4, 4],
                    [0, 8, 2, 4],
                    [0, 0, 4, 0],
                    [0, 0, 0, 0]], True
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
