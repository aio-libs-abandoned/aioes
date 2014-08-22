import asyncio
import unittest
from aioes import Elasticsearch
from aioes.exception import NotFoundError

import pprint
pp = pprint.pprint

MESSAGES = [
    {
        "user": "Johny Mnemonic",
        "birthDate": "2109-11-15T14:12:12",
        "message": "trying out Elasticsearch",
        "skills": ["Python", "PHP", "HTML", "C++", ".NET", "JavaScript"],
        "counter": 0
    },
    {
        "user": "Sidor Spiridonovich",
        "birthDate": "2009-01-11T11:02:11",
        "message": "trying in Elasticsearch",
        "skills": ["Java", "1C", "C++", ".NET", "JavaScript"],
        "counter": 0
    },
    {
        "user": "Fedor Poligrafovich",
        "birthDate": "1969-12-15T14:12:12",
        "message": "trying out everything",
        "skills": ["MODULA", "ADA", "PLM", "BASIC", "Python"],
        "counter": 0
    },
]

class TestClient(unittest.TestCase):
    def setUp(self):
        self._index = 'test_elasticsearch'
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.cl = Elasticsearch([{'host': 'localhost'}], loop=self.loop)
        self.addCleanup(self.cl.close)
        try:
            self.loop.run_until_complete(self.cl.delete(self._index, '', ''))
        except NotFoundError:
            pass

    def tearDown(self):
        self.loop.close()

    def test_index(self):
        """ index """
        @asyncio.coroutine
        def go():
            data = yield from self.cl.index(self._index, 'tweet', {}, '1')
            self.assertEqual(data['_index'], self._index)
            self.assertEqual(data['_type'], 'tweet')
            self.assertEqual(data['_id'], '1')
            self.assertEqual(data['_version'], 1)
            self.assertEqual(data['created'], True)
             # test bulk version
            data = yield from self.cl.index(self._index, 'tweet', {}, '1')
            self.assertEqual(data['_index'], self._index)
            self.assertEqual(data['_type'], 'tweet')
            self.assertEqual(data['_id'], '1')
            self.assertEqual(data['_version'], 2)
            self.assertEqual(data['created'], False)
        self.loop.run_until_complete(go())

    def test_exist(self):
        """ exists """
        @asyncio.coroutine
        def go():
            id = '100'
            # test non-exist
            data = yield from self.cl.exists(self._index, id)
            self.assertFalse(data)
            # test exist
            yield from self.cl.index(self._index, 'exist', {}, id)
            data = yield from self.cl.exists(self._index, id)
            self.assertTrue(data)
        self.loop.run_until_complete(go())

    def test_get(self):
        """ get """
        @asyncio.coroutine
        def go():
            id = '200'
            yield from self.cl.index(self._index, 'test_get', MESSAGES[1], id)
            data = yield from self.cl.get(self._index, id)
            self.assertEqual(data['_id'], id)
            self.assertEqual(data['_index'], self._index)
            self.assertEqual(data['_type'], 'test_get')
            self.assertEqual(data['_version'], 1)
            self.assertEqual(data['found'], True)
            self.assertEqual(data['_source'], MESSAGES[1])
        self.loop.run_until_complete(go())

    def test_update(self):
        """ update """
        @asyncio.coroutine
        def go():
            script = {
                "doc": {
                    "counter": 123
                }
            }
            yield from self.cl.index(self._index, 'testdoc', MESSAGES[2], '1')
            data = yield from self.cl.update(self._index, 'testdoc', '1', script)
            data = yield from self.cl.get(self._index, '1')
            self.assertEqual(data['_source']['counter'], 123)
            self.assertEqual(data['_version'], 2)
        self.loop.run_until_complete(go())

    def test_get_source(self):
        """ get_source """
        @asyncio.coroutine
        def go():
            id = '200'
            yield from self.cl.index(self._index, 'test_get_source', MESSAGES[2], id)
            data = yield from self.cl.get_source(self._index, id)
            self.assertEqual(data, MESSAGES[2])
        self.loop.run_until_complete(go())

#    def test_mget(self):
#        """ mget """
#        @asyncio.coroutine
#        def go():
#            body = {"ids": ['200', '2']}
#            yield from self.cl.index(self._index, 'test_mget', MESSAGES[0], '200')
#            data = yield from self.cl.mget(body, index=self._index)
#            import ipdb; ipdb.set_trace()
#        self.loop.run_until_complete(go())


    # def test_(self):
    #     @asyncio.coroutine
    #     def go():
    #         pass
    #     self.loop.run_until_complete(go())
