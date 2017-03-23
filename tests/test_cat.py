import asyncio

import pytest


INDEX = 'test_elasticsearch'


@asyncio.coroutine
def test_aliases(client):
    ret = yield from client.cat.aliases(v=True)
    assert 'alias' in ret
    assert 'index' in ret


@asyncio.coroutine
def test_allocation(client):
    ret = yield from client.cat.allocation(v=True)
    assert 'disk.percent' in ret


@asyncio.coroutine
def test_count(client):
    ret = yield from client.cat.count(v=True)
    assert 'timestamp' in ret
    assert 'count' in ret

    # testing for index
    yield from client.create(
        INDEX, 'tweet',
        {
            'user': 'Bob',
        },
        '1'
    )
    ret = yield from client.cat.count(INDEX, v=True)
    assert 'timestamp' in ret
    assert 'count' in ret


@asyncio.coroutine
def test_health(client):
    ret = yield from client.cat.health(v=True)
    assert 'timestamp' in ret
    assert 'node.total' in ret


@pytest.mark.parametrize('expected_url', [
    '/_cat/aliases',
    '/_cat/allocation',
    '/_cat/count',
    '/_cat/health',
    '/_cat/indices',
    '/_cat/master',
    '/_cat/nodes',
    '/_cat/recovery',
    '/_cat/shards',
    '/_cat/segments',
    '/_cat/pending_tasks',
    '/_cat/thread_pool',
    '/_cat/fielddata',
    '/_cat/plugins',
    ])
@asyncio.coroutine
def test_cat_index(client, expected_url):
    ret = yield from client.cat.help()
    ret = ret.splitlines()
    assert '=^.^=' in ret
    # check that all implemented urls are present
    assert expected_url in ret


@asyncio.coroutine
def test_indices(client):
    ret = yield from client.cat.indices(v=True)
    assert 'health' in ret
    assert 'index' in ret


@asyncio.coroutine
def test_master(client):
    ret = yield from client.cat.master(v=True)
    assert 'host' in ret
    assert 'ip' in ret


@asyncio.coroutine
def test_nodes(client):
    ret = yield from client.cat.nodes(v=True)
    assert 'load' in ret
    assert 'name' in ret


@asyncio.coroutine
def test_recovery(client):
    ret = yield from client.cat.recovery(v=True)
    assert 'index' in ret
    assert 'files' in ret


@asyncio.coroutine
def test_shards(client):
    ret = yield from client.cat.shards(v=True)
    assert 'index' in ret
    assert 'node' in ret


@asyncio.coroutine
def test_segments(client):
    yield from client.create(
        INDEX, 'tweet',
        {
            'user': 'Bob',
        },
        '1'
    )
    ret = yield from client.cat.segments(index=INDEX, v=True)
    assert 'index' in ret
    assert 'segment' in ret


@asyncio.coroutine
def test_pending_tasks(client):
    ret = yield from client.cat.pending_tasks(v=True)
    assert 'insertOrder' in ret
    assert 'priority' in ret


@asyncio.coroutine
def test_thread_pool(client, es_tag):
    ret = yield from client.cat.thread_pool(v=True)
    header = next(map(lambda s: s.split(' '), ret.splitlines()), None)
    assert header is not None
    if es_tag < (5, 0):
        assert 'host' in header
        assert 'ip' in header
    else:
        assert 'node_name' in header


@asyncio.coroutine
def test_fielddata(client):
    ret = yield from client.cat.fielddata(v=True)
    header = next(map(lambda s: s.split(' '), ret.splitlines()), None)
    assert header is not None
    assert 'id' in header
    assert 'host' in header


@asyncio.coroutine
def test_plugins(client):
    ret = yield from client.cat.plugins(v=True)
    assert 'name' in ret
    assert 'component' in ret
