import asyncio
import unittest
from aioes import Elasticsearch
from aioes.exception import NotFoundError


class TestNodes(unittest.TestCase):

    def setUp(self):
        self._index = 'elastic_search'
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.cl = Elasticsearch([{'host': 'localhost'}], loop=self.loop)
        self.addCleanup(self.cl.close)
        try:
            self.loop.run_until_complete(
                self.cl.delete(self._index, refresh=True))
        except NotFoundError:
            pass

    def tearDown(self):
        self.loop.close()

    def test_info(self):
        @asyncio.coroutine
        def go():
            ret = yield from self.cl.nodes.info()
            self.assertIn('cluster_name', ret)

        self.loop.run_until_complete(go())

    def test_stats(self):
        @asyncio.coroutine
        def go():
            ret = yield from self.cl.nodes.stats()
            self.assertIn('nodes', ret)
            self.assertTrue(len(ret['nodes']) > 0)

        self.loop.run_until_complete(go())

    def test_hot_threads(self):
        @asyncio.coroutine
        def go():
            ret = yield from self.cl.nodes.hot_threads()
            self.assertIn('cpu usage by thread', ret)

        self.loop.run_until_complete(go())
