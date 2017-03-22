import asyncio
import pytest
from aioes import Elasticsearch
from aioes.exception import NotFoundError, RequestError


INDEX = 'test_elasticsearch'


@pytest.fixture
def client(es_params, loop):     # XXX: to much clients all over tests;
    client = Elasticsearch([{'host': es_params['host']}], loop=loop)
    try:
        loop.run_until_complete(client.delete(INDEX, '', ''))
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


@pytest.mark.parametrize('kwargs', [
    dict(),
    dict(threads=3),
    dict(type_='cpu'),
    dict(type_='wait'),
    dict(ignore_idle_threads=False),
    dict(ignore_idle_threads='yes'),  # NOTE: value is ignored by elastic
    dict(ignore_idle_threads='ok'),
], ids=repr)
@asyncio.coroutine
def test_hot_threads(client, kwargs):
    ret = yield from client.nodes.hot_threads(**kwargs)
    lines = ret.split("\n\n")
    assert len(lines) >= 2  # Header + empty line
    # It is probable that no data is returned (in es 5.x)
    if lines[1]:
        assert 'cpu usage by thread' in lines[1]


@pytest.mark.parametrize('kwargs', [
    pytest.mark.xfail(
        dict(type_='foobar'),
        reason="empty result is returned"),
    dict(threads='abc'),
    dict(interval='minute'),
], ids=repr)
@asyncio.coroutine
def test_hot_threads__errors(client, kwargs):
    with pytest.raises(RequestError):
        assert (yield from client.nodes.hot_threads(**kwargs)) is None
