import asyncio

import pytest

from aioes import Elasticsearch
from aioes.exception import NotFoundError
import pprint
pp = pprint.pprint


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
def test_health(client):
    data = yield from client.cluster.health()
    assert 'status' in data
    data = yield from client.cluster.health(
        level='indices',
        local=True,
        master_timeout='1s',
        timeout='1s',
        wait_for_active_shards=1,
        wait_for_nodes='>2',
        wait_for_relocating_shards=0)
    assert 'status', data
    with pytest.raises(TypeError):
        yield from client.cluster.health(level=1)
    with pytest.raises(ValueError):
        yield from client.cluster.health(level='1')
    with pytest.raises(TypeError):
        yield from client.cluster.health(wait_for_status=1)
    with pytest.raises(ValueError):
        yield from client.cluster.health(wait_for_status='1')


@asyncio.coroutine
def test_pending_tasks(client):
    data = yield from client.cluster.pending_tasks()
    assert 'tasks' in data


@asyncio.coroutine
def test_state(client, index):
    data = yield from client.cluster.state()
    assert 'routing_nodes' in data
    assert 'master_node' in data

    # create index
    yield from client.create(
        index, 'tweet',
        {
            'user': 'Bob',
        },
        '1'
    )
    data = yield from client.cluster.state(index=index)
    assert 'routing_nodes' in data
    assert 'master_node' in data


@asyncio.coroutine
def test_stats(client):
    data = yield from client.cluster.stats()
    assert 'indices' in data
    assert 'nodes' in data


@asyncio.coroutine
def test_reroute(client, index):
    # create index
    yield from client.create(
        index, 'tweet',
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
                    "index": index,
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
