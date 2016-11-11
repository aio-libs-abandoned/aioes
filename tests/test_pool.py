import asyncio
import random
import time

import pytest

from aioes.pool import RandomSelector, RoundRobinSelector, ConnectionPool
from aioes.transport import Endpoint
from aioes.connection import Connection


def test_random_select():
    random.seed(123456)
    s = RandomSelector()
    r = s.select([1, 2, 3])
    assert 2 == r


def test_round_robin_select():
    s = RoundRobinSelector()
    r = s.select([1, 2, 3])
    assert 2 == r
    r = s.select([1, 2, 3])
    assert 3 == r
    r = s.select([1, 2, 3])
    assert 1 == r
    r = s.select([1, 2, 3])
    assert 2 == r


@pytest.yield_fixture
def make_pool(loop, make_connection):
    pool = None

    def maker(*, connections=...):
        nonlocal pool
        if connections is ...:
            conn = make_connection()
            connections = [conn]
        pool = ConnectionPool(connections, loop=loop)
        return pool

    yield maker

    if pool is not None:
        pool.close()


def test_ctor(make_pool):
    pool = make_pool()
    assert abs(60-pool.dead_timeout) < 1e-6
    assert 5 == pool.timeout_cutoff
    assert 0 == len(pool._dead_count)
    assert pool._dead.empty()


@asyncio.coroutine
def test_full_cycle(make_pool):
    pool = make_pool()
    conn = pool.connections[0]

    yield from pool.mark_dead(conn)
    assert [] == pool.connections
    assert 1 == pool._dead_count[conn]

    yield from pool.resurrect(True)
    assert [conn] == pool.connections
    assert 1 == pool._dead_count[conn]

    yield from pool.mark_dead(conn)
    assert [] == pool.connections
    assert 2 == pool._dead_count[conn]

    yield from pool.resurrect(True)
    assert [conn] == pool.connections
    assert 2 == pool._dead_count[conn]

    yield from pool.mark_live(conn)
    assert [conn] == pool.connections
    assert 0 == pool._dead_count[conn]


@asyncio.coroutine
def test_mark_dead(make_pool):
    pool = make_pool()
    conn = pool.connections[0]

    t0 = time.monotonic() + pool.dead_timeout
    yield from pool.mark_dead(conn)
    t1 = time.monotonic() + pool.dead_timeout
    assert [] == pool.connections
    assert not pool._dead.empty()
    assert 1 == pool._dead_count[conn]
    timeout, conn2 = yield from pool._dead.get()
    assert conn is conn2
    assert t0 <= timeout <= t1, (t0, timeout, t1)


@asyncio.coroutine
def test_mark_dead_unknown(make_pool):
    pool = make_pool()
    conn = pool.connections[0]
    yield from pool.mark_dead("unknown")
    assert 0 == len(pool._dead_count)
    assert pool._dead.empty()
    assert [conn] == pool.connections


@asyncio.coroutine
def test_mark_dead_twice(make_pool):
    pool = make_pool()
    conn = pool.connections[0]

    pool._dead_count[conn] = 1

    t0 = time.monotonic() + pool.dead_timeout * 2
    yield from pool.mark_dead(conn)
    t1 = time.monotonic() + pool.dead_timeout * 2
    assert [] == pool.connections
    assert not pool._dead.empty()
    assert 2 == pool._dead_count[conn]
    timeout, conn2 = yield from pool._dead.get()
    assert conn is conn2
    assert t0 <= timeout <= t1, (t0, timeout, t1)


@asyncio.coroutine
def test_mark_dead_after_cutoff(make_pool):
    pool = make_pool()
    conn = pool.connections[0]

    pool._dead_count[conn] = 7

    t0 = time.monotonic() + pool.dead_timeout * 2 ** 5
    yield from pool.mark_dead(conn)
    t1 = time.monotonic() + pool.dead_timeout * 2 ** 5
    assert [] == pool.connections
    assert not pool._dead.empty()
    assert 8 == pool._dead_count[conn]
    timeout, conn2 = yield from pool._dead.get()
    assert conn is conn2
    assert t0 <= timeout <= t1, (t0, timeout, t1)


@asyncio.coroutine
def test_mark_live(make_pool, make_connection):
    pool = make_pool(connections=[])
    conn = make_connection()

    yield from pool.mark_live(conn)
    assert conn not in pool._dead_count


@asyncio.coroutine
def test_mark_live_dead(make_pool, make_connection):
    pool = make_pool(connections=[])
    conn = make_connection()

    pool._dead_count[conn] = 1

    yield from pool.mark_live(conn)
    assert conn not in pool._dead_count


@asyncio.coroutine
def test_resurrect(loop, make_pool):
    c1 = Connection(Endpoint('http', 'h1', 1), loop=loop)
    c2 = Connection(Endpoint('http', 'h2', 2), loop=loop)
    pool = make_pool(connections=[c1, c2])

    yield from pool.mark_dead(c1)
    yield from pool.mark_dead(c2)
    yield from pool.resurrect()
    assert 2 == pool._dead.qsize()
    yield from pool.resurrect(True)
    assert 1 == pool._dead.qsize()
    assert [c1] == pool.connections


@asyncio.coroutine
def test_get_connection(loop, make_pool):
    c1 = Connection(Endpoint('http', 'h1', 1), loop=loop)
    c2 = Connection(Endpoint('http', 'h2', 2), loop=loop)
    pool = make_pool(connections=[c1, c2])

    yield from pool.mark_dead(c1)
    yield from pool.mark_dead(c2)

    conn = yield from pool.get_connection()
    assert 1 == pool._dead.qsize()
    assert c1 is conn
