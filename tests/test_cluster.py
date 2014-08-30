import asyncio
import unittest
from aioes import Elasticsearch
from aioes.exception import NotFoundError
import pprint
pp = pprint.pprint


class TestCluster(unittest.TestCase):
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

    def test_health(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.cluster.health()
            self.assertIn('status', data)
            data = yield from self.cl.cluster.health(
                level='indices',
                local=True,
                master_timeout='1s',
                timeout='1s',
                wait_for_active_shards=1,
                wait_for_nodes='>2',
                wait_for_relocating_shards=0)
            self.assertIn('status', data)
            with self.assertRaises(TypeError):
                yield from self.cl.cluster.health(level=1)
            with self.assertRaises(ValueError):
                yield from self.cl.cluster.health(level='1')
            with self.assertRaises(TypeError):
                yield from self.cl.cluster.health(wait_for_status=1)
            with self.assertRaises(ValueError):
                yield from self.cl.cluster.health(wait_for_status='1')

        self.loop.run_until_complete(go())
