import uuid
import socket
import time

import pytest
from docker import Client as DockerClient

from aioes.connection import Connection
from aioes.transport import Endpoint


@pytest.fixture(scope='session')
def session_id():
    '''Unique session identifier, random string.'''
    return str(uuid.uuid4())


@pytest.fixture(scope='session')
def docker():
    return DockerClient(version='auto')


def pytest_addoption(parser):
    parser.addoption("--es_tag", action="append", default=[],
                     help=("Elasticsearch server versions. "
                           "May be used several times. "
                           "Available values: 1.6, 1.7, 2.0, "
                           "2.1, 2.2, 2.3, 2.4, 5.0, all"))
    parser.addoption("--no-pull", action="store_true", default=False,
                     help="Don't perform docker images pulling")


def pytest_generate_tests(metafunc):
    if 'es_tag' in metafunc.fixturenames:
        tags = set(metafunc.config.option.es_tag)
        if not tags:
            tags = ['2.4']
        elif 'all' in tags:
            tags = ['1.6', '1.7', '2.0', '2.1', '2.2', '2.3', '2.4', '5.0']
        else:
            tags = list(tags)
        metafunc.parametrize("es_tag", tags, scope='session')


@pytest.yield_fixture(scope='session')
def es_server(docker, session_id, es_tag, request):
    if not request.config.option.no_pull:
        docker.pull('elasticsearch:{}'.format(es_tag))
    container = docker.create_container(
        image='elasticsearch:{}'.format(es_tag),
        name='aioes-test-server-{}-{}'.format(es_tag, session_id),
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
