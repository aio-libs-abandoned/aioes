import asyncio
import unittest
from aioes import Elasticsearch
from aioes.exception import NotFoundError, RequestError
import pprint
pp = pprint.pprint

MESSAGE = {
    "user": "Johny Mnemonic",
    "birthDate": "2109-11-15T14:12:12",
    "message": "trying out Elasticsearch",
    "skills": ["Python", "PHP", "HTML", "C++", ".NET", "JavaScript"],
    "counter": 0,
    "test_field": "this, is a test 125 !"}


class TestIndices(unittest.TestCase):
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

    def test_analize(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.indices.analyze(
                text='this, is a test 125 !',
                analyzer='standard',
                filters='lowercase')
            self.assertEqual(len(data['tokens']), 5)
            self.assertEqual(data['tokens'][0]['token'], 'this')
            self.assertEqual(data['tokens'][1]['token'], 'is')
            self.assertEqual(data['tokens'][2]['token'], 'a')
            self.assertEqual(data['tokens'][3]['token'], 'test')
            self.assertEqual(data['tokens'][4]['token'], '125')
            self.assertEqual(data['tokens'][4]['type'], '<NUM>')

            data = yield from self.cl.indices.analyze(
                text='this is a <b>test</b>',
                tokenizer='keyword',
                token_filters='lowercase',
                char_filters='html_strip',
                prefer_local=True)
            self.assertEqual(data['tokens'][0]['token'], 'this is a test')

            with self.assertRaises(RequestError):
                yield from self.cl.indices.analyze(
                    analyzer='standard',
                    filters='lowercase',
                    field='w')

        self.loop.run_until_complete(go())

    def test_create(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.indices.create(
                self._index, timeout=1000, master_timeout=1000)
            self.assertTrue(data['acknowledged'])
        self.loop.run_until_complete(go())

    def test_refresh(self):
        @asyncio.coroutine
        def go():
            yield from self.cl.index(self._index, 'type', MESSAGE, '1')
            data = yield from self.cl.indices.refresh(self._index)
            self.assertIn('_shards', data, data)
            yield from self.cl.indices.refresh(
                self._index,
                allow_no_indices=False, expand_wildcards='closed',
                ignore_unavailable=True, ignore_indices='', force=True)
            with self.assertRaises(TypeError):
                yield from self.cl.indices.refresh(
                    self._index, expand_wildcards=1)
            with self.assertRaises(ValueError):
                yield from self.cl.indices.refresh(
                    self._index, expand_wildcards='1')
        self.loop.run_until_complete(go())

    def test_flush(self):
        @asyncio.coroutine
        def go():
            yield from self.cl.index(self._index, 'type', MESSAGE, '1')
            data = yield from self.cl.indices.flush(self._index)
            self.assertIn('_shards', data, data)
            yield from self.cl.indices.flush(
                self._index, full=True,
                allow_no_indices=False, expand_wildcards='closed',
                ignore_unavailable=True, ignore_indices='', force=True)
            with self.assertRaises(TypeError):
                yield from self.cl.indices.flush(
                    self._index, expand_wildcards=1)
            with self.assertRaises(ValueError):
                yield from self.cl.indices.flush(
                    self._index, expand_wildcards='1')
        self.loop.run_until_complete(go())

    def test_open(self):
        @asyncio.coroutine
        def go():
            yield from self.cl.indices.create(self._index)
            data = yield from self.cl.indices.open(
                self._index, timeout=1000, master_timeout=1000,
                allow_no_indices=False, expand_wildcards='closed',
                ignore_unavailable=True)
            self.assertTrue(data['acknowledged'], data)
            data = yield from self.cl.indices.open(self._index)
            with self.assertRaises(TypeError):
                yield from self.cl.indices.open(self._index,
                                                expand_wildcards=1,
                                                ignore_unavailable=True)
            with self.assertRaises(ValueError):
                yield from self.cl.indices.open(self._index,
                                                expand_wildcards='1')
        self.loop.run_until_complete(go())

    def test_close(self):
        @asyncio.coroutine
        def go():
            yield from self.cl.index(self._index, 'type',
                                     MESSAGE,
                                     '1')
            yield from self.cl.cluster.health(
                self._index,
                wait_for_status='yellow')
            data = yield from self.cl.indices.close(self._index)
            self.assertTrue(data['acknowledged'], data)

            data = yield from self.cl.indices.close(
                self._index,
                timeout='1s', master_timeout='1s',
                expand_wildcards='open',
                allow_no_indices=True,
                ignore_unavailable=True)
            self.assertTrue(data['acknowledged'], data)
            with self.assertRaises(TypeError):
                yield from self.cl.indices.close(
                    self._index,
                    expand_wildcards=1)
            with self.assertRaises(ValueError):
                yield from self.cl.indices.close(
                    self._index,
                    expand_wildcards='1')

        self.loop.run_until_complete(go())

    def test_delete(self):
        @asyncio.coroutine
        def go():
            yield from self.cl.index(self._index, 'type', MESSAGE, '1')
            data = yield from self.cl.indices.delete(self._index)
            self.assertTrue(data['acknowledged'], data)
            with self.assertRaises(NotFoundError):
                yield from self.cl.indices.delete(
                    self._index, timeout='1s', master_timeout='1s')
            self.assertTrue(data['acknowledged'], data)
        self.loop.run_until_complete(go())

    def test_exists(self):
        @asyncio.coroutine
        def go():
            yield from self.cl.index(self._index, 'type', MESSAGE, '1')
            data = yield from self.cl.indices.exists(
                self._index,
                allow_no_indices=False,
                expand_wildcards='closed',
                ignore_unavailable=False,
                local=False)
            self.assertTrue(data)
            data = yield from self.cl.indices.exists(self._index+'123')
            self.assertFalse(data)
            with self.assertRaises(TypeError):
                yield from self.cl.indices.exists(
                    self._index, expand_wildcards=1)
            with self.assertRaises(ValueError):
                yield from self.cl.indices.exists(
                    self._index, expand_wildcards='1')

        self.loop.run_until_complete(go())

    def test_exists_type(self):
        @asyncio.coroutine
        def go():
            yield from self.cl.index(self._index, 'type', MESSAGE, '1')
            # yield from self.cl.cluster.health(
            #     self._index,
            #     wait_for_status='green')
            data = yield from self.cl.indices.exists_type(
                self._index, 'type')
            # self.assertTrue(data)
            data = yield from self.cl.indices.exists_type(
                self._index, 'ert', expand_wildcards='open')
            self.assertFalse(data)
            with self.assertRaises(TypeError):
                yield from self.cl.indices.exists_type(
                    self._index, '', expand_wildcards=1,
                    allow_no_indices=True,
                    ignore_unavailable=True,
                    ignore_indices=True,
                    local=True)
            with self.assertRaises(ValueError):
                yield from self.cl.indices.exists_type(
                    self._index, '', expand_wildcards='1')

        self.loop.run_until_complete(go())

    # def test_get_settings(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.get_settings()
    #     self.loop.run_until_complete(go())
    #
    # def test_put_settings(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.index(self._index, 'type', MESSAGE, '1')
    #         # yield from self.cl.indices.put_settings(self._index)
    #     self.loop.run_until_complete(go())
    #
    # def test_status(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.status()
    #     self.loop.run_until_complete(go())
    #
    # def test_stats(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.stats()
    #     self.loop.run_until_complete(go())
    #
    # def test_segments(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.segments()
    #     self.loop.run_until_complete(go())
    #
    # def test_optimize(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.optimize()
    #     self.loop.run_until_complete(go())
    #
    # def test_validate_query(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.validate_query()
    #     self.loop.run_until_complete(go())
    #
    # def test_clear_cache(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.clear_cache()
    #     self.loop.run_until_complete(go())
    #
    # def test_recovery(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.recovery()
    #     self.loop.run_until_complete(go())
    #
    # def test_snapshot_index(self):
    #     @asyncio.coroutine
    #     def go():
    #         # yield from self.cl.indices.snapshot_index()
    #         pass
    #     self.loop.run_until_complete(go())

    # ************************
    # ************************
    #
    # def test_put_warmer(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.put_warmer()
    #     self.loop.run_until_complete(go())
    #
    # def test_get_warmer(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.get_warmer()
    #     self.loop.run_until_complete(go())
    #
    # def test_delete_warmer(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.delete_warmer()
    #     self.loop.run_until_complete(go())
    # def test_put_mapping(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.put_mapping()
    #     self.loop.run_until_complete(go())
    #
    # def test_get_mapping(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.get_mapping()
    #     self.loop.run_until_complete(go())
    #
    # def test_get_field_mapping(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.get_field_mapping()
    #     self.loop.run_until_complete(go())
    #
    # def test_delete_mapping(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.delete_mapping()
    #     self.loop.run_until_complete(go())
    #
    # def test_put_alias(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.put_alias()
    #     self.loop.run_until_complete(go())
    #
    # def test_exists_alias(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.exists_alias()
    #     self.loop.run_until_complete(go())
    #
    # def test_get_alias(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.get_alias()
    #     self.loop.run_until_complete(go())
    #
    # def test_get_aliases(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.get_aliases()
    #     self.loop.run_until_complete(go())
    #
    # def test_update_aliases(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.update_aliases()
    #     self.loop.run_until_complete(go())
    #
    # def test_delete_alias(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.delete_alias()
    #     self.loop.run_until_complete(go())
    #
    # def test_put_template(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.put_template()
    #     self.loop.run_until_complete(go())
    #
    # def test_exists_template(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.exists_template()
    #     self.loop.run_until_complete(go())
    #
    # def test_get_template(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.get_template()
    #     self.loop.run_until_complete(go())
    #
    # def test_delete_template(self):
    #     @asyncio.coroutine
    #     def go():
    #         yield from self.cl.indices.delete_template()
    #     self.loop.run_until_complete(go())
