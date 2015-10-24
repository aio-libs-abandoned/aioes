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
            yield from self.cl.indices.refresh(self._index)
            data = yield from self.cl.indices.exists_type(
                self._index, 'type', allow_no_indices=False)
            self.assertTrue(data)
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

    def test_get_settings(self):
        @asyncio.coroutine
        def go():
            yield from self.cl.index(self._index, 'type', MESSAGE, '1')
            yield from self.cl.indices.refresh(self._index)
            data = yield from self.cl.indices.get_settings()
            self.assertIn(self._index, data)
            data = yield from self.cl.indices.get_settings(
                expand_wildcards='open',
                ignore_indices='',
                flat_settings=False,
                ignore_unavailable=False,
                local=True)
            self.assertIn(self._index, data)
            with self.assertRaises(TypeError):
                yield from self.cl.indices.get_settings(expand_wildcards=1)
            with self.assertRaises(ValueError):
                yield from self.cl.indices.get_settings(expand_wildcards='1')

        self.loop.run_until_complete(go())

    def test_put_settings(self):
        @asyncio.coroutine
        def go():
            yield from self.cl.index(self._index, 'type', MESSAGE, '1')
            yield from self.cl.indices.refresh(self._index)
            data = yield from self.cl.indices.put_settings(
                {"index": {"number_of_replicas": 2}}, self._index)
            self.assertTrue(data['acknowledged'], data)
            with self.assertRaises(RequestError):
                yield from self.cl.indices.put_settings(
                    {"index": {"number_of_replicas": 2}},
                    allow_no_indices=True,
                    expand_wildcards='open',
                    flat_settings=False,
                    ignore_unavailable=False,
                    master_timeout='1s')
            self.assertTrue(data['acknowledged'], data)
            with self.assertRaises(TypeError):
                yield from self.cl.indices.put_settings(
                    {}, expand_wildcards=1)
            with self.assertRaises(ValueError):
                yield from self.cl.indices.put_settings(
                    {}, expand_wildcards='1')

        self.loop.run_until_complete(go())

    def test_status(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.indices.status()
            self.assertIn('indices', data)
            data = yield from self.cl.indices.status(
                ignore_indices='',
                allow_no_indices=True,
                recovery=False,
                snapshot=False,
                operation_threading='',
                expand_wildcards='open',
                ignore_unavailable=False,
                human=True)
            self.assertIn('_shards', data)
            with self.assertRaises(TypeError):
                yield from self.cl.indices.status(expand_wildcards=1)
            with self.assertRaises(ValueError):
                yield from self.cl.indices.status(expand_wildcards='1')

        self.loop.run_until_complete(go())

    def test_stats(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.indices.stats()
            self.assertIn('indices', data, data)
            data = yield from self.cl.indices.stats(
                metric='_all',
                completion_fields='*',
                docs=1,
                fielddata_fields='*',
                fields='*',
                groups='*',
                allow_no_indices=True,
                expand_wildcards='open',
                ignore_indices=False,
                ignore_unavailable=True,
                level='cluster',
                types='*',
                human=True)
            self.assertIn('_all', data, data)
            with self.assertRaises(TypeError):
                yield from self.cl.indices.stats(expand_wildcards=1)
            with self.assertRaises(ValueError):
                yield from self.cl.indices.stats(expand_wildcards='1')
            with self.assertRaises(TypeError):
                yield from self.cl.indices.stats(level=1)
            with self.assertRaises(ValueError):
                yield from self.cl.indices.stats(level='1')
            with self.assertRaises(TypeError):
                yield from self.cl.indices.stats(metric=1)
            with self.assertRaises(ValueError):
                yield from self.cl.indices.stats(metric='1')
        self.loop.run_until_complete(go())

    def test_segments(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.indices.segments()
            self.assertIn('indices', data, data)
            self.assertIn('_shards', data, data)
            data = yield from self.cl.indices.segments(
                allow_no_indices=True,
                ignore_indices=True,
                ignore_unavailable=True,
                expand_wildcards='open',
                human=True)
            self.assertIn('indices', data, data)
            self.assertIn('_shards', data, data)
            with self.assertRaises(TypeError):
                yield from self.cl.indices.segments(expand_wildcards=1)
            with self.assertRaises(ValueError):
                yield from self.cl.indices.segments(expand_wildcards='1')

        self.loop.run_until_complete(go())

    def test_optimize(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.indices.optimize()
            self.assertIn('_shards', data)
            data = yield from self.cl.indices.optimize(
                allow_no_indices=True,
                expand_wildcards='open',
                ignore_indices=True,
                ignore_unavailable=True,
                max_num_segments=0,
                only_expunge_deletes=True,
                operation_threading='',
                wait_for_merge=False,
                force=True,
                flush=True)
            self.assertIn('_shards', data)
            with self.assertRaises(TypeError):
                yield from self.cl.indices.optimize(expand_wildcards=1)
            with self.assertRaises(ValueError):
                yield from self.cl.indices.optimize(expand_wildcards='1')
        self.loop.run_until_complete(go())

    def test_validate_query(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.indices.validate_query()
            self.assertIn('_shards', data)
            yield from self.cl.indices.validate_query(
                explain=True,
                allow_no_indices=True,
                q='',
                ignore_indices=True,
                source='',
                operation_threading='',
                expand_wildcards='open',
                ignore_unavailable=False)
            with self.assertRaises(TypeError):
                yield from self.cl.indices.validate_query(expand_wildcards=1)
            with self.assertRaises(ValueError):
                yield from self.cl.indices.validate_query(expand_wildcards='1')
        self.loop.run_until_complete(go())

    def test_clear_cache(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.indices.clear_cache()
            self.assertIn('_shards', data)
            yield from self.cl.indices.clear_cache(
                field_data=True,
                fielddata=True,
                recycler=True,
                id_cache=True,
                filter_keys='',
                filter_cache=True,
                filter=False,
                fields='',
                id=False,
                allow_no_indices=False,
                ignore_indices=False,
                ignore_unavailable=True,
                expand_wildcards='open')
            self.assertIn('_shards', data)
            with self.assertRaises(TypeError):
                yield from self.cl.indices.clear_cache(expand_wildcards=1)
            with self.assertRaises(ValueError):
                yield from self.cl.indices.clear_cache(expand_wildcards='1')
        self.loop.run_until_complete(go())

    def test_recovery(self):
        @asyncio.coroutine
        def go():
            yield from self.cl.index(self._index, 'type', MESSAGE, '1')
            data = yield from self.cl.indices.refresh(self._index)
            data = yield from self.cl.indices.recovery()
            self.assertIn(self._index, data)
            data = yield from self.cl.indices.recovery(
                active_only=False,
                detailed=True,
                human=True)
        self.loop.run_until_complete(go())

    def test_mapping(self):
        @asyncio.coroutine
        def go():
            yield from self.cl.indices.create(self._index)
            mapping = {
                'testdoc': {
                    'properties': {
                        'message': {
                            'type': 'string',
                        }
                    }
                }
            }
            # PUT
            data = yield from self.cl.indices.put_mapping(
                self._index,
                'testdoc',
                mapping,
            )
            self.assertTrue(data['acknowledged'])

            # GET
            data = yield from self.cl.indices.get_mapping(
                self._index,
                'testdoc',
            )
            self.assertEqual(data['elastic_search']['mappings'], mapping)

            # DELETE
            yield from self.cl.indices.delete_mapping(
                self._index,
                'testdoc',
            )
            data = yield from self.cl.indices.get_mapping(
                self._index,
                'testdoc',
            )
            self.assertFalse(data)

        self.loop.run_until_complete(go())

    def test_get_field_mapping(self):
        @asyncio.coroutine
        def go():
            # create index
            yield from self.cl.index(self._index, 'type', MESSAGE, '1')
            rt = yield from self.cl.indices.get_field_mapping(
                'message', index=self._index
            )
            self.assertEqual(
                # dude, you are so deep
                rt[self._index]['mappings']['type']['message']['mapping'],
                {'message': {'type': 'string'}}
            )
        self.loop.run_until_complete(go())

    def test_warmers(self):
        @asyncio.coroutine
        def go():
            # create index
            yield from self.cl.index(self._index, 'type', MESSAGE, '1')

            a = yield from self.cl.indices.get_warmer(name='warmer')
            self.assertFalse(a)

            b = {
                "query": {
                    "match_all": {}
                },
                "aggs": {
                    "aggs_1": {
                        "terms": {
                            "field": "message"
                        }
                    }
                }
            }
            yield from self.cl.indices.put_warmer(
                index=self._index, name='warmer', body=b
            )

            a = yield from self.cl.indices.get_warmer(name='warmer')
            self.assertIn('warmer', a[self._index]['warmers'].keys())

            yield from self.cl.indices.delete_warmer(
                name='warmer', index=self._index
            )
            a = yield from self.cl.indices.get_warmer(name='warmer')
            self.assertFalse(a)

        self.loop.run_until_complete(go())

    def test_aliases(self):
        @asyncio.coroutine
        def go():
            # create index
            yield from self.cl.index(self._index, 'type', MESSAGE, '1')

            al = yield from self.cl.indices.exists_alias('alias')
            self.assertFalse(al)
            al = yield from self.cl.indices.get_alias('alias')
            self.assertEqual({}, al)
            al = yield from self.cl.indices.get_aliases('alias')
            self.assertEqual({}, al)

            yield from self.cl.indices.put_alias('alias', self._index)
            al = yield from self.cl.indices.exists_alias('alias')
            self.assertTrue(al)
            yield from self.cl.indices.update_aliases(body={
                "actions": [
                    {"remove": {"index": self._index, "alias": "alias"}},
                    {"add": {"index": self._index, "alias": "alias2"}}
                ]
            })
            al = yield from self.cl.indices.exists_alias('alias2')
            self.assertTrue(al)
            yield from self.cl.indices.delete_alias(self._index, 'alias2')
            al = yield from self.cl.indices.get_aliases('alias')
            self.assertFalse(al)
        self.loop.run_until_complete(go())

    def test_templates(self):
        @asyncio.coroutine
        def go():
            b = {
                "template": self._index,
                "settings": {
                    "number_of_shards": '1'
                },
            }
            t = yield from self.cl.indices.exists_template('template')
            self.assertFalse(t)
            yield from self.cl.indices.put_template('template', b)
            t = yield from self.cl.indices.exists_template('template')
            self.assertTrue(t)
            t = yield from self.cl.indices.get_template('template')
            self.assertEqual(
                t['template']['settings']['index.number_of_shards'],
                b['settings']['number_of_shards']
            )
            yield from self.cl.indices.delete_template('template')
            t = yield from self.cl.indices.exists_template('template')
            self.assertFalse(t)
        self.loop.run_until_complete(go())
