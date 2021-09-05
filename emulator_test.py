import unittest
from emulator.emulator_core import random_tile_generate, pure_move
from emulator.emulator_api import check_state, get_new_max


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

class EmulatorAPITest(unittest.TestCase):
    def test_get_new_max(self):
        s_0 = [[0, 2, 4, 2],
            [0, 0, 2, 2],
            [0, 0, 0, 2],
            [2, 8, 4, 2]]
        s_1 = [[2, 2, 4, 4],
            [0, 8, 2, 4],
            [0, 0, 4, 0],
            [0, 0, 0, 0]]
        actual = get_new_max(s_0, s_1)
        expected = 4
        self.assertEqual(actual, expected)
    
        s_0 = [ [0, 2, 4, 2],
                [0, 0, 2, 2],
                [32, 32, 0, 2],
                [128, 8, 4, 2]]
        s_1 = [ [2, 4, 2, 0],
                [4, 0, 0, 0],
                [64, 2, 0, 0],
                [128, 8, 4, 2]]
        actual = get_new_max(s_0, s_1)
        expected = 64
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    test_classes_to_run = [EmulatorTest, EmulatorAPITest]
    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)
        
    test_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(test_suite)
