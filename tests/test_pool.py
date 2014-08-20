import random
import unittest

from aioes.pool import RandomSelector, RoundRobinSelector


class TestRandomSelector(unittest.TestCase):

    def setUp(self):
        random.seed(123456)

    def tearDown(self):
        random.seed(None)

    def test_select(self):
        s = RandomSelector()
        r = s.select([1, 2, 3])
        self.assertEqual(2, r)


class TestRoundRobinSelector(unittest.TestCase):

    def test_select(self):
        s = RoundRobinSelector()
        r = s.select([1, 2, 3])
        self.assertEqual(2, r)
        r = s.select([1, 2, 3])
        self.assertEqual(3, r)
        r = s.select([1, 2, 3])
        self.assertEqual(1, r)
        r = s.select([1, 2, 3])
        self.assertEqual(2, r)
