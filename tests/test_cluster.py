import asyncio

import pytest

from aioes import Elasticsearch
from aioes.exception import NotFoundError


INDEX = 'test_elasticsearch'


@pytest.fixture
def client(es_params, loop):
    client = Elasticsearch([
        {'host': es_params['host'], 'port': es_params['port']}],
        loop=loop)
    try:
        loop.run_until_complete(client.delete(INDEX, '', ''))
    except NotFoundError:
        pass
    yield client
    client.close()


@asyncio.coroutine
def test_health(client):
    data = yield from client.cluster.health()
    assert 'status' in data
    data = yield from client.cluster.health(
        level='indices',
        local=True,
        master_timeout='1s',
        timeout='1s',
        # wait_for_active_shards=1, # XXX: verify there are some shards
        # wait_for_nodes='>2',  # XXX: must verify nodes count
        wait_for_relocating_shards=0)
    assert 'status' in data


@pytest.mark.parametrize('error,kwargs', [
    (TypeError, dict(level=1)),
    (ValueError, dict(level='1')),
    (TypeError, dict(wait_for_status=1)),
    (ValueError, dict(wait_for_status='1')),
    ], ids=repr)
@asyncio.coroutine
def test_health_errors(client, error, kwargs):
    with pytest.raises(error):
        yield from client.cluster.health(**kwargs)


@asyncio.coroutine
def test_pending_tasks(client):
    data = yield from client.cluster.pending_tasks()
    assert 'tasks' in data


@asyncio.coroutine
def test_state(client):
    data = yield from client.cluster.state()
    assert 'routing_nodes' in data
    assert 'master_node' in data

    # create index
    yield from client.create(
        INDEX, 'tweet',
        {
            'user': 'Bob',
        },
        '1'
    )
    data = yield from client.cluster.state(index=INDEX)
    assert 'routing_nodes' in data
    assert 'master_node' in data


@asyncio.coroutine
def test_stats(client):
    data = yield from client.cluster.stats()
    assert 'indices' in data
    assert 'nodes' in data


@asyncio.coroutine
def test_reroute(client):
    # create index
    yield from client.create(
        INDEX, 'tweet',
        {
            'user': 'Bob',
        },
        '1'
    )

    # get node's name
    nodes = yield from client.nodes.info()
    node = list(nodes['nodes'].keys())[0]

    b = {
        "commands": [
            {
                "cancel": {
                    "index": INDEX,
                    "shard": 1,
                    "node": node,
                    'allow_primary': True,
                }
            }
        ]
    }
    data = yield from client.cluster.reroute(body=b, dry_run=True)
    assert data['acknowledged']


@asyncio.coroutine
def test_get_settings(client):
    data = yield from client.cluster.get_settings()
    assert 'persistent' in data
    assert 'transient' in data


@asyncio.coroutine
def test_put_settings(client):
    b = {
        "transient": {
            "cluster.routing.allocation.enable": "all"
        }
    }
    data = yield from client.cluster.put_settings(b)
    routing_settings = data['transient']['cluster']['routing']
    assert routing_settings['allocation']['enable'] == 'all'
