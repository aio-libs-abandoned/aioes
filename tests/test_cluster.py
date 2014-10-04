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

    def test_pending_tasks(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.cluster.pending_tasks()
            self.assertIn('tasks', data)

        self.loop.run_until_complete(go())

    def test_state(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.cluster.state()
            self.assertIn('routing_nodes', data)
            self.assertIn('master_node', data)

            # create index
            yield from self.cl.create(
                self._index, 'tweet',
                {
                    'user': 'Bob',
                },
                '1'
            )
            data = yield from self.cl.cluster.state(index=self._index)
            self.assertIn('routing_nodes', data)
            self.assertIn('master_node', data)

        self.loop.run_until_complete(go())

    def test_stats(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.cluster.stats()
            self.assertIn('indices', data)
            self.assertIn('nodes', data)

        self.loop.run_until_complete(go())

    def test_reroute(self):
        @asyncio.coroutine
        def go():
            # create index
            yield from self.cl.create(
                self._index, 'tweet',
                {
                    'user': 'Bob',
                },
                '1'
            )

            # get node's name
            nodes = yield from self.cl.nodes.info()
            node = list(nodes['nodes'].keys())[0]

            b = {
                "commands": [
                    {
                        "cancel": {
                            "index": self._index,
                            "shard": 1,
                            "node": node,
                            'allow_primary': True,
                        }
                    }
                ]
            }
            data = yield from self.cl.cluster.reroute(body=b, dry_run=True)
            self.assertTrue(data['acknowledged'])

        self.loop.run_until_complete(go())

    def test_get_settings(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.cluster.get_settings()
            self.assertIn('persistent', data)
            self.assertIn('transient', data)

        self.loop.run_until_complete(go())

    def test_put_settings(self):
        @asyncio.coroutine
        def go():
            b = {
                "transient": {
                    "cluster.routing.allocation.enable": "all"
                }
            }
            data = yield from self.cl.cluster.put_settings(b)
            routing_settings = data['transient']['cluster']['routing']
            self.assertEqual(
                routing_settings['allocation']['enable'],
                'all'
            )

        self.loop.run_until_complete(go())
