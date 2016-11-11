import asyncio
from unittest import mock

import pytest

from aioes.connection import Connection
# 400 404 409
from aioes.exception import (TransportError, RequestError,
                             NotFoundError, ConflictError)
from aioes.transport import Endpoint


def test_ctor(loop):
    c = Connection(Endpoint('http', 'host', 9999), loop=loop)
    assert Endpoint('http', 'host', 9999) == c.endpoint


@asyncio.coroutine
def test_bad_status_common(loop):
    conn = Connection(Endpoint('http', 'host', 9999), loop=loop)
    resp = mock.Mock()
    resp.status = 401
    r2 = asyncio.Future(loop=loop)
    r2.set_result('{"a": 1}')
    resp.text.return_value = r2
    fut = asyncio.Future(loop=loop)
    fut.set_result(resp)
    conn._session.request = mock.Mock(return_value=fut)

    with pytest.raises(TransportError) as ctx:
        yield from conn.perform_request('GET', '/data', None, None)
    assert 401 == ctx.value.status_code
    assert '{"a": 1}' == ctx.value.error
    assert {"a": 1} == ctx.value.info


@asyncio.coroutine
def test_bad_json(loop):
    conn = Connection(Endpoint('http', 'host', 9999), loop=loop)
    resp = mock.Mock()
    resp.status = 401
    r2 = asyncio.Future(loop=loop)
    r2.set_result('error text')
    resp.text.return_value = r2
    fut = asyncio.Future(loop=loop)
    fut.set_result(resp)
    conn._session.request = mock.Mock(return_value=fut)

    with pytest.raises(TransportError) as ctx:
        yield from conn.perform_request('GET', '/data', None, None)
    assert 401 == ctx.value.status_code
    assert 'error text' == ctx.value.error
    assert ctx.value.info is None


@asyncio.coroutine
def test_bad_status_400(loop):
    conn = Connection(Endpoint('http', 'host', 9999), loop=loop)
    resp = mock.Mock()
    resp.status = 400
    r2 = asyncio.Future(loop=loop)
    r2.set_result('{"a": 1}')
    resp.text.return_value = r2
    fut = asyncio.Future(loop=loop)
    fut.set_result(resp)
    conn._session.request = mock.Mock(return_value=fut)

    with pytest.raises(RequestError) as ctx:
        yield from conn.perform_request('GET', '/data', None, None)
    assert 400 == ctx.value.status_code
    assert '{"a": 1}' == ctx.value.error
    assert {"a": 1} == ctx.value.info


@asyncio.coroutine
def test_bad_status_404(loop):
    conn = Connection(Endpoint('http', 'host', 9999), loop=loop)
    resp = mock.Mock()
    resp.status = 404
    r2 = asyncio.Future(loop=loop)
    r2.set_result('{"a": 1}')
    resp.text.return_value = r2
    fut = asyncio.Future(loop=loop)
    fut.set_result(resp)
    conn._session.request = mock.Mock(return_value=fut)

    with pytest.raises(NotFoundError) as ctx:
        yield from conn.perform_request('GET', '/data', None, None)
    assert 404 == ctx.value.status_code
    assert '{"a": 1}' == ctx.value.error
    assert {"a": 1} == ctx.value.info


@asyncio.coroutine
def test_bad_status_409(loop):
    conn = Connection(Endpoint('http', 'host', 9999), loop=loop)
    resp = mock.Mock()
    resp.status = 409
    r2 = asyncio.Future(loop=loop)
    r2.set_result('{"a": 1}')
    resp.text.return_value = r2
    fut = asyncio.Future(loop=loop)
    fut.set_result(resp)
    conn._session.request = mock.Mock(return_value=fut)

    with pytest.raises(ConflictError) as ctx:
        yield from conn.perform_request('GET', '/data', None, None)
    assert 409 == ctx.value.status_code
    assert '{"a": 1}' == ctx.value.error
    assert {"a": 1} == ctx.value.info
