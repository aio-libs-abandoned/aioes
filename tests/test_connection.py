import asyncio
import unittest
from unittest import mock

from aioes.connection import Connection
# 400 404 409
from aioes.exception import (TransportError, RequestError,
                             NotFoundError, ConflictError)
from aioes.transport import Endpoint
from asyncio.test_utils import TestLoop


class TestConnection(unittest.TestCase):

    def setUp(self):
        self.loop = TestLoop()

    def test_ctor(self):
        c = Connection(Endpoint('http', 'host', 9999), loop=self.loop)
        self.assertEqual(Endpoint('http', 'host', 9999), c.endpoint)

    def test_bad_status_common(self):

        @asyncio.coroutine
        def go():
            conn = Connection(Endpoint('http', 'host', 9999), loop=self.loop)
            resp = mock.Mock()
            resp.status = 401
            r2 = asyncio.Future(loop=self.loop)
            r2.set_result('{"a": 1}')
            resp.text.return_value = r2
            fut = asyncio.Future(loop=self.loop)
            fut.set_result(resp)
            conn._session.request = mock.Mock(return_value=fut)

            with self.assertRaises(TransportError) as ctx:
                yield from conn.perform_request('GET', '/data', None, None)
            self.assertEqual(401, ctx.exception.status_code)
            self.assertEqual('{"a": 1}', ctx.exception.error)
            self.assertEqual({"a": 1}, ctx.exception.info)

        self.loop.run_until_complete(go())

    def test_bad_json(self):

        @asyncio.coroutine
        def go():
            conn = Connection(Endpoint('http', 'host', 9999), loop=self.loop)
            resp = mock.Mock()
            resp.status = 401
            r2 = asyncio.Future(loop=self.loop)
            r2.set_result('error text')
            resp.text.return_value = r2
            fut = asyncio.Future(loop=self.loop)
            fut.set_result(resp)
            conn._session.request = mock.Mock(return_value=fut)

            with self.assertRaises(TransportError) as ctx:
                yield from conn.perform_request('GET', '/data', None, None)
            self.assertEqual(401, ctx.exception.status_code)
            self.assertEqual('error text', ctx.exception.error)
            self.assertEqual(None, ctx.exception.info)

        self.loop.run_until_complete(go())

    def test_bad_status_400(self):

        @asyncio.coroutine
        def go():
            conn = Connection(Endpoint('http', 'host', 9999), loop=self.loop)
            resp = mock.Mock()
            resp.status = 400
            r2 = asyncio.Future(loop=self.loop)
            r2.set_result('{"a": 1}')
            resp.text.return_value = r2
            fut = asyncio.Future(loop=self.loop)
            fut.set_result(resp)
            conn._session.request = mock.Mock(return_value=fut)

            with self.assertRaises(RequestError) as ctx:
                yield from conn.perform_request('GET', '/data', None, None)
            self.assertEqual(400, ctx.exception.status_code)
            self.assertEqual('{"a": 1}', ctx.exception.error)
            self.assertEqual({"a": 1}, ctx.exception.info)

        self.loop.run_until_complete(go())

    def test_bad_status_404(self):

        @asyncio.coroutine
        def go():
            conn = Connection(Endpoint('http', 'host', 9999), loop=self.loop)
            resp = mock.Mock()
            resp.status = 404
            r2 = asyncio.Future(loop=self.loop)
            r2.set_result('{"a": 1}')
            resp.text.return_value = r2
            fut = asyncio.Future(loop=self.loop)
            fut.set_result(resp)
            conn._session.request = mock.Mock(return_value=fut)

            with self.assertRaises(NotFoundError) as ctx:
                yield from conn.perform_request('GET', '/data', None, None)
            self.assertEqual(404, ctx.exception.status_code)
            self.assertEqual('{"a": 1}', ctx.exception.error)
            self.assertEqual({"a": 1}, ctx.exception.info)

        self.loop.run_until_complete(go())

    def test_bad_status_409(self):

        @asyncio.coroutine
        def go():
            conn = Connection(Endpoint('http', 'host', 9999), loop=self.loop)
            resp = mock.Mock()
            resp.status = 409
            r2 = asyncio.Future(loop=self.loop)
            r2.set_result('{"a": 1}')
            resp.text.return_value = r2
            fut = asyncio.Future(loop=self.loop)
            fut.set_result(resp)
            conn._session.request = mock.Mock(return_value=fut)

            with self.assertRaises(ConflictError) as ctx:
                yield from conn.perform_request('GET', '/data', None, None)
            self.assertEqual(409, ctx.exception.status_code)
            self.assertEqual('{"a": 1}', ctx.exception.error)
            self.assertEqual({"a": 1}, ctx.exception.info)

        self.loop.run_until_complete(go())
