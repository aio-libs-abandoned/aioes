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

    def test_allocation(self):
        @asyncio.coroutine
        def go():
            ret = yield from self.cl.cat.allocation(v=True)
            self.assertIn('disk.percent', ret)

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
