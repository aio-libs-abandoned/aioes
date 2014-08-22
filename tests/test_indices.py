import asyncio
import unittest
from aioes import Elasticsearch
from aioes.exception import NotFoundError

import pprint
pp = pprint.pprint
import ipdb

class TestIndices(unittest.TestCase):
    def setUp(self):
        self._index = 'elastic_search'
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

    def test_analize(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.indices.analyze(
                text='this, is a test 125 !',
                analyzer='standard')
            self.assertEqual(len(data['tokens']), 5)
            self.assertEqual(data['tokens'][0]['token'], 'this')
            self.assertEqual(data['tokens'][1]['token'], 'is')
            self.assertEqual(data['tokens'][2]['token'], 'a')
            self.assertEqual(data['tokens'][3]['token'], 'test')
            self.assertEqual(data['tokens'][4]['token'], '125')
            self.assertEqual(data['tokens'][4]['type'], '<NUM>')
        self.loop.run_until_complete(go())


    def test_create(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.indices.create(self._index)
            self.assertEqual(data['acknowledged'], True)
        self.loop.run_until_complete(go())

    def test_open(self):
        @asyncio.coroutine
        def go():
            yield from self.cl.indices.create(self._index)
            data = yield from self.cl.indices.open(self._index)
            self.assertEqual(data['acknowledged'], True)
        self.loop.run_until_complete(go())

    # def test_close(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.create(self._index)
    #         data = yield from self.cl.indices.close(self._index)
    #         self.assertEqual(data['acknowledged'], True)
    #     self.loop.run_until_complete(go())


    # def test_(self):
    #     @asyncio.coroutine
    #     def go():
    #         pass
    #     self.loop.run_until_complete(go())
