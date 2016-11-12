import asyncio
import time
import urllib.parse
import pytest

from aioes.transport import Endpoint, Transport


@pytest.fixture
def make_transport(loop, es_params):
    tr = None

    def maker(endpoints=[{'host': es_params['host']}], sniffer_interval=None):
        nonlocal tr
        tr = Transport(endpoints, loop=loop,
                       sniffer_interval=sniffer_interval)
        return tr
    yield maker
    if tr is not None:
        tr.close()


def test_ctor(make_transport, es_params):
    tr = make_transport()
    assert 3 == tr.max_retries
    assert time.monotonic() >= tr.last_sniff
    assert tr.sniffer_interval is None
    assert 0.1 == tr.sniffer_timeout
    assert [Endpoint('http', es_params['host'], 9200)] == tr.endpoints
    assert 1 == len(tr._pool.connections)


@asyncio.coroutine
def test_simple(make_transport):
    tr = make_transport()
    status, data = yield from tr.perform_request(
        'GET', '/_nodes/_all/clear')
    assert 200 == status
    assert 'nodes' in data
    # self.assertEqual(
    #     {'nodes':
    #      {'kagIbHGHS3a0dcyPmp0Jkw':
    #       {'version': '1.3.1',
    #        'ip': '127.0.1.1',
    #        'build': '2de6dc5',
    #        'name': 'Mandrill',
    #        'transport_address':
    #        'inet[/192.168.0.183:9300]',
    #        'http_address': 'inet[/192.168.0.183:9200]',
    #        'host': 'andrew-levelup'}},
    #      'cluster_name': 'elasticsearch'}, data)


def test_set_endpoints(make_transport):
    tr = make_transport([])
    assert [] == tr.endpoints
    tr.endpoints = [{'host': 'localhost'}]
    assert [Endpoint('http', 'localhost', 9200)] == tr.endpoints
    assert 1 == len(tr._pool.connections)


def test_set_endpoints_Endpoint(make_transport):
    tr = make_transport([])
    assert [] == tr.endpoints
    tr.endpoints = [Endpoint('http', 'localhost', 9200)]
    assert [Endpoint('http', 'localhost', 9200)] == tr.endpoints
    assert 1 == len(tr._pool.connections)


def test_dont_recreate_existing_connections(make_transport):
    tr = make_transport()
    tr.endpoints = [{'host': 'localhost'}]
    assert [Endpoint('http', 'localhost', 9200)] == tr.endpoints


def test_set_malformed_endpoints(make_transport, es_params):
    tr = make_transport()
    with pytest.raises(RuntimeError):
        tr.endpoints = [123]
    assert [Endpoint('http', es_params['host'], 9200)] == tr.endpoints
    assert 1 == len(tr._pool.connections)


def test_set_host_only_string(make_transport):
    tr = make_transport()
    tr.endpoints = ['host']
    assert [Endpoint('http', 'host', 9200)] == tr.endpoints
    assert 1 == len(tr._pool.connections)


def test_set_host_port_string(make_transport):
    tr = make_transport()
    tr.endpoints = ['host:123']
    assert [Endpoint('http', 'host', 123)] == tr.endpoints
    assert 1 == len(tr._pool.connections)


def test_set_host_port_string_invalid(make_transport, es_params):
    tr = make_transport()
    with pytest.raises(RuntimeError):
        tr.endpoints = ['host:123:abc']
    assert [Endpoint('http', es_params['host'], 9200)] == tr.endpoints
    assert 1 == len(tr._pool.connections)


def test_set_host_dict_invalid(make_transport, es_params):
    tr = make_transport()
    with pytest.raises(RuntimeError):
        tr.endpoints = [{'a': 'b'}]
    assert [Endpoint('http', es_params['host'], 9200)] == tr.endpoints
    assert 1 == len(tr._pool.connections)


def test_username_password_endpoints_with_port(make_transport):
    tr = make_transport(endpoints=['john:doe@localhost:9200'])
    assert [Endpoint('http', 'john:doe@localhost', 9200)] == tr.endpoints


def test_username_password_endpoints_without_port(make_transport):
    tr = make_transport(endpoints=['john:doe@localhost'])
    assert [Endpoint('http', 'john:doe@localhost', 9200)] == tr.endpoints


def test_username_password_endpoints_with_port_https(make_transport):
    tr = make_transport(endpoints=['https://john:doe@localhost:9200'])
    assert [Endpoint('https', 'john:doe@localhost', 9200)] == tr.endpoints
    assert ('https', 'john:doe@localhost:9200', '/', '', '', '') == \
        tuple(urllib.parse.urlparse(tr._pool.connections[0]._base_url))


def test_bad_schema(make_transport):
    with pytest.raises(RuntimeError):
        make_transport(endpoints=['s3://john:doe@localhost:9200'])


def test_default_port_https(make_transport):
    tr = make_transport(endpoints=['https://localhost'])
    assert [Endpoint('https', 'localhost', 443)] == tr.endpoints


def test_default_port_http(make_transport):
    tr = make_transport(endpoints=['http://localhost'])
    assert [Endpoint('http', 'localhost', 9200)] == tr.endpoints


@asyncio.coroutine
def test_sniff(make_transport, loop):
    tr = make_transport(sniffer_interval=0.001)

    t0 = time.monotonic()
    yield from asyncio.sleep(0.001, loop=loop)
    yield from tr.get_connection()
    assert tr.last_sniff > t0


@asyncio.coroutine
def test_get_connection_without_sniffing(make_transport):
    tr = make_transport(sniffer_interval=1000)

    t0 = tr.last_sniff
    yield from tr.get_connection()
    assert t0 == tr.last_sniff


@asyncio.coroutine
def test_perform_request_body_bytes(make_transport):
    tr = make_transport()

    status, data = yield from tr.perform_request(
        'GET', '/_nodes/_all', body=b'')

    assert status == 200
