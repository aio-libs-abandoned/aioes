import random
import unittest

from aioes.pool import RandomSelector


class TestRandomSelector(unittest.TestCase):

    def setUp(self):
        random.seed(123456)

    def tearDown(self):
        random.seed(None)

    def test_select(self):
        s = RandomSelector()
        r = s.select([1, 2, 3])
        self.assertEqual(2, r)
