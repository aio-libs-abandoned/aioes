import uuid
import socket
import time

import pytest
from contextlib import closing
from docker import Client as DockerClient

from aioes import Elasticsearch
from aioes.connection import Connection
from aioes.transport import Endpoint
from aioes.exception import NotFoundError


@pytest.fixture(scope='session')
def session_id():
    '''Unique session identifier, random string.'''
    return str(uuid.uuid4())


@pytest.fixture(scope='session')
def docker(request):
    if request.config.getoption('--no-docker'):
        return None
    return DockerClient(version='auto')


ELASTIC_TAGS = []


def pytest_addoption(parser):
    parser.addoption("--no-docker", action="store_true", default=False,
                     help="Do not use docker,"
                          " use local elasticsearch instance"
                          " with address (localhost:9200)")
    parser.addoption("--es-tag", action="append", default=[],
                     help=("Elasticsearch server versions. "
                           "May be used several times. "
                           "Available values: 1.6, 1.7, 2.0, "
                           "2.1, 2.2, 2.3, 2.4, 5.0, all"))
    parser.addoption("--no-pull", action="store_true", default=False,
                     help="Don't perform docker images pulling")


def pytest_configure(config):
    tags = config.getoption('--es-tag')
    ELASTIC_TAGS[:] = tags or ['2.4']


def pytest_collection_modifyitems(session, config, items):
    for item in items:
        if 'es_tag' in item.keywords:
            marker = item.keywords['es_tag']
            min_tag = marker.kwargs.get('min')
            max_tag = marker.kwargs.get('max')
            cur = item.callspec.getparam('es_tag')
            if isinstance(cur, str):
                cur = tuple(map(int, cur.split('.')))
            reason = marker.kwargs.get('reason', "Skip by version")
            if min_tag and max_tag:
                if not (min_tag <= cur < max_tag):
                    item.add_marker(pytest.mark.skip(reason=reason))
            elif min_tag:
                if cur < min_tag:
                    item.add_marker(pytest.mark.skip(reason=reason))
            elif max_tag:
                if cur >= max_tag:
                    item.add_marker(pytest.mark.skip(reason=reason))


@pytest.fixture(scope='session', params=ELASTIC_TAGS, ids='ESv{}'.format)
def es_tag(request):
    return tuple(map(int, request.param.split('.')))


@pytest.fixture(scope='session')
def es_server(docker, session_id, es_tag, request):
    if request.config.getoption('--no-docker'):
        yield dict(es_params=dict(host='localhost', port=9200))
    else:
        tag = '.'.join(map(str, es_tag))
        if not request.config.option.no_pull:
            docker.pull('elasticsearch:{}'.format(tag))
        container = docker.create_container(
            image='elasticsearch:{}'.format(tag),
            name='aioes-test-server-{}-{}'.format(tag, session_id),
            ports=[9200],
            detach=True,
        )
        docker.start(container=container['Id'])
        inspection = docker.inspect_container(container['Id'])
        host = inspection['NetworkSettings']['IPAddress']
        es_params = dict(host=host,
                         port=9200)

        delay = 0.001
        for i in range(100):
            try:
                s = socket.socket()
                s.connect((host, 9200))
                break
            except OSError:
                time.sleep(delay)
                delay *= 2
        else:
            pytest.fail("Cannot start elasticsearch server")
        container['host'] = host
        container['port'] = 9200
        container['es_params'] = es_params
        yield container

        docker.kill(container=container['Id'])
        docker.remove_container(container['Id'])


@pytest.fixture
def es_params(es_server):
    return dict(**es_server['es_params'])


@pytest.fixture()
def make_connection(loop, es_params):

    conns = []

    def go(*, no_loop=False, **kwargs):
        nonlocal conn

        conn = Connection(Endpoint('http',
                                   es_params['host'],
                                   es_params['port']),
                          loop=loop)
        conns.append(conn)
        return conn

    yield go

    for conn in conns:
        conn.close()


@pytest.fixture
def client(es_params, loop):
    with closing(Elasticsearch([{'host': es_params['host']}], loop=loop)) as c:
        INDEX = 'test_elasticsearch'
        try:
            loop.run_until_complete(c.delete(INDEX, '', ''))
        except NotFoundError:
            pass
        yield c
