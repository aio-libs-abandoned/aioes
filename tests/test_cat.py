import asyncio
import unittest
import textwrap
from aioes import Elasticsearch
from aioes.exception import NotFoundError


class TestCat(unittest.TestCase):

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

    def test_aliases(self):
        @asyncio.coroutine
        def go():
            ret = yield from self.cl.cat.aliases(v=True)
            self.assertIn('alias', ret)
            self.assertIn('index', ret)

        self.loop.run_until_complete(go())

    def test_allocation(self):
        @asyncio.coroutine
        def go():
            ret = yield from self.cl.cat.allocation(v=True)
            self.assertIn('disk.percent', ret)

        self.loop.run_until_complete(go())

    def test_count(self):
        @asyncio.coroutine
        def go():
            ret = yield from self.cl.cat.count(v=True)
            self.assertIn('timestamp', ret)
            self.assertIn('count', ret)

            # testing for index
            yield from self.cl.create(
                self._index, 'tweet',
                {
                    'user': 'Bob',
                },
                '1'
            )
            ret = yield from self.cl.cat.count(self._index, v=True)
            self.assertIn('timestamp', ret)
            self.assertIn('count', ret)

        self.loop.run_until_complete(go())

    def test_health(self):
        @asyncio.coroutine
        def go():
            ret = yield from self.cl.cat.health(v=True)
            self.assertIn('timestamp', ret)
            self.assertIn('node.total', ret)

        self.loop.run_until_complete(go())

    def test_help(self):
        pattern = textwrap.dedent("""\
                                  =^.^=
                                  /_cat/allocation
                                  /_cat/shards
                                  /_cat/shards/{index}
                                  /_cat/master
                                  /_cat/nodes
                                  /_cat/indices
                                  /_cat/indices/{index}
                                  /_cat/segments
                                  /_cat/segments/{index}
                                  /_cat/count
                                  /_cat/count/{index}
                                  /_cat/recovery
                                  /_cat/recovery/{index}
                                  /_cat/health
                                  /_cat/pending_tasks
                                  /_cat/aliases
                                  /_cat/aliases/{alias}
                                  /_cat/thread_pool
                                  /_cat/plugins
                                  /_cat/fielddata
                                  /_cat/fielddata/{fields}
                                  """)

        @asyncio.coroutine
        def go():
            ret = yield from self.cl.cat.help(help=True)
            self.assertEqual(pattern, ret)

        self.loop.run_until_complete(go())
