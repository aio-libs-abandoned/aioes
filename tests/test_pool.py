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


default = object()


class TestConnectionPool(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def make_pool(self, connections=default):
        if connections is default:
            connections = [Connection(Endpoint('http', 'localhost', 9200),
                                      loop=self.loop)]
        pool = ConnectionPool(connections, loop=self.loop)
        self.addCleanup(pool.close)
        return pool

    def test_ctor(self):
        pool = self.make_pool()
        self.assertAlmostEqual(60, pool.dead_timeout)
        self.assertEqual(5, pool.timeout_cutoff)
        self.assertEqual(0, len(pool._dead_count))
        self.assertTrue(pool._dead.empty())

    def test_full_cycle(self):

        @asyncio.coroutine
        def go():
            pool = self.make_pool()
            conn = pool.connections[0]

            yield from pool.mark_dead(conn)
            self.assertEqual([], pool.connections)
            self.assertEqual(1, pool._dead_count[conn])

            yield from pool.resurrect(True)
            self.assertEqual([conn], pool.connections)
            self.assertEqual(1, pool._dead_count[conn])

            yield from pool.mark_dead(conn)
            self.assertEqual([], pool.connections)
            self.assertEqual(2, pool._dead_count[conn])

            yield from pool.resurrect(True)
            self.assertEqual([conn], pool.connections)
            self.assertEqual(2, pool._dead_count[conn])

            yield from pool.mark_live(conn)
            self.assertEqual([conn], pool.connections)
            self.assertEqual(0, pool._dead_count[conn])

        self.loop.run_until_complete(go())

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

    def test_mark_dead_twice(self):

        @asyncio.coroutine
        def go():
            pool = self.make_pool()
            conn = pool.connections[0]

            pool._dead_count[conn] = 1

            t0 = time.monotonic() + pool.dead_timeout * 2
            yield from pool.mark_dead(conn)
            t1 = time.monotonic() + pool.dead_timeout * 2
            self.assertEqual([], pool.connections)
            self.assertFalse(pool._dead.empty())
            self.assertEqual(2, pool._dead_count[conn])
            timeout, conn2 = yield from pool._dead.get()
            self.assertIs(conn, conn2)
            self.assertTrue(t0 <= timeout <= t1, (t0, timeout, t1))

        self.loop.run_until_complete(go())

    def test_mark_dead_after_cutoff(self):

        @asyncio.coroutine
        def go():
            pool = self.make_pool()
            conn = pool.connections[0]

            pool._dead_count[conn] = 7

            t0 = time.monotonic() + pool.dead_timeout * 2 ** 5
            yield from pool.mark_dead(conn)
            t1 = time.monotonic() + pool.dead_timeout * 2 ** 5
            self.assertEqual([], pool.connections)
            self.assertFalse(pool._dead.empty())
            self.assertEqual(8, pool._dead_count[conn])
            timeout, conn2 = yield from pool._dead.get()
            self.assertIs(conn, conn2)
            self.assertTrue(t0 <= timeout <= t1, (t0, timeout, t1))

        self.loop.run_until_complete(go())

    def test_mark_live(self):

        @asyncio.coroutine
        def go():
            pool = self.make_pool(connections=[])
            conn = Connection(Endpoint('http', 'localhost', 9200),
                              loop=self.loop)

            yield from pool.mark_live(conn)
            self.assertNotIn(conn, pool._dead_count)

        self.loop.run_until_complete(go())

    def test_mark_live_dead(self):

        @asyncio.coroutine
        def go():
            pool = self.make_pool(connections=[])
            conn = Connection(Endpoint('http', 'localhost', 9200),
                              loop=self.loop)
            pool._dead_count[conn] = 1

            yield from pool.mark_live(conn)
            self.assertNotIn(conn, pool._dead_count)

        self.loop.run_until_complete(go())

    def test_resurrect(self):

        @asyncio.coroutine
        def go():
            c1 = Connection(Endpoint('http', 'h1', 1), loop=self.loop)
            c2 = Connection(Endpoint('http', 'h2', 2), loop=self.loop)
            pool = self.make_pool(connections=[c1, c2])

            yield from pool.mark_dead(c1)
            yield from pool.mark_dead(c2)
            yield from pool.resurrect()
            self.assertEqual(2, pool._dead.qsize())
            yield from pool.resurrect(True)
            self.assertEqual(1, pool._dead.qsize())
            self.assertEqual([c1], pool.connections)

        self.loop.run_until_complete(go())

    def test_get_connection(self):

        @asyncio.coroutine
        def go():
            c1 = Connection(Endpoint('http', 'h1', 1), loop=self.loop)
            c2 = Connection(Endpoint('http', 'h2', 2), loop=self.loop)
            pool = self.make_pool(connections=[c1, c2])

            yield from pool.mark_dead(c1)
            yield from pool.mark_dead(c2)

            conn = yield from pool.get_connection()
            self.assertEqual(1, pool._dead.qsize())
            self.assertIs(c1, conn)

        self.loop.run_until_complete(go())
