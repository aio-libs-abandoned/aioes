import asyncio
import random
import time
import unittest

from aioes.pool import RandomSelector, RoundRobinSelector, ConnectionPool
from aioes.transport import Endpoint
from aioes.connection import Connection


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


class TestConnectionPool(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def make_pool(self):
        conn = Connection(Endpoint('localhost', 9200), loop=self.loop)
        pool = ConnectionPool([conn], loop=self.loop)
        self.addCleanup(pool.close)
        return pool

    def test_ctor(self):
        pool = self.make_pool()
        self.assertAlmostEqual(60, pool.dead_timeout)
        self.assertEqual(5, pool.timeout_cutoff)
        self.assertEqual(0, len(pool._dead_count))
        self.assertTrue(pool._dead.empty())

    def test_mark_dead(self):

        @asyncio.coroutine
        def go():
            pool = self.make_pool()
            conn = pool.connections[0]

            t0 = time.monotonic() + pool.dead_timeout
            yield from pool.mark_dead(conn)
            t1 = time.monotonic() + pool.dead_timeout
            self.assertEqual([], pool.connections)
            self.assertFalse(pool._dead.empty())
            self.assertEqual(1, pool._dead_count[conn])
            timeout, conn2 = yield from pool._dead.get()
            self.assertIs(conn, conn2)
            self.assertTrue(t0 <= timeout <= t1, (t0, timeout, t1))

        self.loop.run_until_complete(go())

    def test_mark_dead_unknown(self):

        @asyncio.coroutine
        def go():
            pool = self.make_pool()
            conn = pool.connections[0]
            yield from pool.mark_dead("unknown")
            self.assertEqual(0, len(pool._dead_count))
            self.assertTrue(pool._dead.empty())
            self.assertEqual([conn], pool.connections)

        self.loop.run_until_complete(go())
