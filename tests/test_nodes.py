import asyncio
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
def test_info(client):
    ret = yield from client.nodes.info()
    assert 'cluster_name' in ret


@asyncio.coroutine
def test_stats(client):
    ret = yield from client.nodes.stats()
    assert 'nodes' in ret
    assert len(ret['nodes']) > 0


@asyncio.coroutine
def test_hot_threads(client):
    ret = yield from client.nodes.hot_threads()
    assert 'cpu usage by thread' in ret
