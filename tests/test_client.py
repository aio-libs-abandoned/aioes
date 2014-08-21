import asyncio
import unittest
from aioes import Elasticsearch
from aioes.exception import NotFoundError


class TestClient(unittest.TestCase):
    def setUp(self):
        self._index = 'test_elasticsearch'
        self._body = {"user": "kimchy",
                      "post_date": "2009-11-15T14:12:12",
                      "message": "trying out Elasticsearch"}
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.cl = Elasticsearch([{'host': 'localhost'}], loop=self.loop)
        self.addCleanup(self.cl.close)
        try:
            self.delete(self._index, '', '')
        except NotFoundError:
            return False

    def tearDown(self):
        self.loop.close()

    def delete(self, index, doctype, id):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.delete(index, doctype, id)
            return data
        return self.loop.run_until_complete(go())

    def make_rec(self, doctype, id, _body=None):
        @asyncio.coroutine
        def go():
            body = self._body
            if _body is not None:
                body = _body
            data = yield from self.cl.index(self._index, doctype, body, id)
            return data
        return self.loop.run_until_complete(go())

    def test_index(self):
        """ index """
        data = self.make_rec('tweet', '1')
        self.assertEqual(data['_index'], self._index)
        self.assertEqual(data['_type'], 'tweet')
        self.assertEqual(data['_id'], '1')
        self.assertEqual(data['_version'], 1)
        self.assertEqual(data['created'], True)
        # test bulk version
        data = self.make_rec('tweet', '1')
        self.assertEqual(data['_index'], self._index)
        self.assertEqual(data['_type'], 'tweet')
        self.assertEqual(data['_id'], '1')
        self.assertEqual(data['_version'], 2)
        self.assertEqual(data['created'], False)

    def test_exist(self):
        """ exists """
        @asyncio.coroutine
        def go(id):
            data = yield from self.cl.exists(self._index, id)
            return data

        id = '100'
        # test non-exist
        data = self.loop.run_until_complete(go(id))
        self.assertFalse(data)
        # test exist
        self.make_rec('exist', id)
        data = self.loop.run_until_complete(go(id))
        self.assertTrue(data)

    def test_get(self):
        """ get """
        @asyncio.coroutine
        def go(id):
            data = yield from self.cl.get(self._index, id)
            return data

        id = '200'
        self.make_rec('test_get', id)
        data = self.loop.run_until_complete(go(id))
        self.assertEqual(data['_id'], id)
        self.assertEqual(data['_index'], self._index)
        self.assertEqual(data['_type'], 'test_get')
        self.assertEqual(data['_version'], 1)
        self.assertEqual(data['found'], True)
        self.assertEqual(data['_source'], self._body)
