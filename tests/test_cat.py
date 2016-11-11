import asyncio
import textwrap

import pytest


from aioes import Elasticsearch
from aioes.exception import NotFoundError


@pytest.fixture
def index():
    return 'test_elasticsearch'


@pytest.fixture
def client(es_params, index, loop):
    client = Elasticsearch([{'host': es_params['host']}], loop=loop)
    try:
        loop.run_until_complete(client.delete(index, '', ''))
    except NotFoundError:
        pass
    yield client
    client.close()


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
        index, 'tweet',
        {
            'user': 'Bob',
        },
        '1'
    )
    ret = yield from client.cat.count(index, v=True)
    assert 'timestamp' in ret
    assert 'count' in ret


@asyncio.coroutine
def test_health(client):
    ret = yield from client.cat.health(v=True)
    assert 'timestamp' in ret
    assert 'node.total' in ret


@asyncio.coroutine
def test_help(client):
    pattern = textwrap.dedent("""\
                              =^.^=
                              /_cat/allocation
                              /_cat/shards
                              /_cat/shards/{index}
                              /_cat/master
                              /_cat/nodes
                              /_cat/indices
                              /_cat/indices/{index}
                              /_cat/segments
                              /_cat/segments/{index}
                              /_cat/count
                              /_cat/count/{index}
                              /_cat/recovery
                              /_cat/recovery/{index}
                              /_cat/health
                              /_cat/pending_tasks
                              /_cat/aliases
                              /_cat/aliases/{alias}
                              /_cat/thread_pool
                              /_cat/plugins
                              /_cat/fielddata
                              /_cat/fielddata/{fields}
                              """)

    ret = yield from client.cat.help(help=True)
    assert pattern == ret


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
        index, 'tweet',
        {
            'user': 'Bob',
        },
        '1'
    )
    ret = yield from client.cat.segments(index=index, v=True)
    assert 'index' in ret
    assert 'segment' in ret


@asyncio.coroutine
def test_pending_tasks(client):
    ret = yield from client.cat.pending_tasks(v=True)
    assert 'insertOrder' in ret
    assert 'priority' in ret


@asyncio.coroutine
def test_thread_pool(client):
    ret = yield from client.cat.thread_pool(v=True)
    assert 'host' in ret
    assert 'ip' in ret


@asyncio.coroutine
def test_fielddata(client):
    ret = yield from client.cat.fielddata(v=True)
    assert 'id' in ret
    assert 'total' in ret


@asyncio.coroutine
def test_plugins(client):
    ret = yield from client.cat.plugins(v=True)
    assert 'name' in ret
    assert 'component' in ret
