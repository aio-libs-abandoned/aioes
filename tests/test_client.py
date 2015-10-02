import asyncio
import unittest
from aioes import Elasticsearch
from aioes.exception import (NotFoundError, ConflictError,
                             RequestError, TransportError)

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
    {
        "user": "Super",
        "birthDate": "1912-11-15T14:12:12",
        "message": "trying out ssdff  everything",
        "skills": ["MODULA", "ADA", "PLM", "BASIC", "Python"],
        "counter": 10
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

    def test_ping(self):
        """ ping """

        class R:
            @asyncio.coroutine
            def perform_request(self, a, b):
                yield
                raise TransportError

            def close(self):
                pass

        @asyncio.coroutine
        def go():
            data = yield from self.cl.ping()
            self.assertTrue(data)
            self.cl._transport = R()
            yield from self.cl.ping()
        self.loop.run_until_complete(go())
        self.cl.__repr__()

    def test_info(self):
        """ test_info """
        @asyncio.coroutine
        def go():
            data = yield from self.cl.info()
            self.assertEqual(data['status'], 200)
        self.loop.run_until_complete(go())

    def test_create(self):
        """ create index """
        @asyncio.coroutine
        def go():
            data = yield from self.cl.create(
                self._index, 'tweet',
                {
                    'user': 'Bob',
                    'skills': ['C', 'Python', 'Assembler'],
                    'date': '2009-11-15T14:12:12'
                },
                '1',
                routing='Bob')
            self.assertEqual(data['_index'], self._index)
            self.assertEqual(data['_type'], 'tweet')
            self.assertEqual(data['_version'], 1)
            self.assertTrue(data['created'], data)
            # test for conflict
            with self.assertRaises(ConflictError):
                yield from self.cl.create(
                    self._index, 'tweet', {}, '1')
        self.loop.run_until_complete(go())

    def test_index(self):
        """ auto-create index """
        @asyncio.coroutine
        def go():
            data = yield from self.cl.index(self._index, 'tweet', {}, '1')
            self.assertEqual(data['_index'], self._index)
            self.assertEqual(data['_type'], 'tweet')
            self.assertEqual(data['_id'], '1')
            self.assertEqual(data['_version'], 1)
            self.assertTrue(data['created'], data)
            # test increment version
            data = yield from self.cl.index(self._index, 'tweet', {}, '1')
            self.assertEqual(data['_version'], 2)
            self.assertFalse(data['created'], data)
            # test 'external' version_type
            data = yield from self.cl.index(self._index, 'tweet', {}, '12',
                                            version_type='external',
                                            version=122,
                                            timestamp='2009-11-15T14:12:12',
                                            ttl='1d',
                                            consistency='one',
                                            timeout=30000,
                                            refresh=True,
                                            replication='async')
            self.assertEqual(data['_version'], 122)
            self.assertTrue(data['created'], data)
            with self.assertRaises(RequestError):
                yield from self.cl.index(self._index, 'type', {},
                                         parent='1',
                                         percolate='')
            with self.assertRaises(TypeError):
                yield from self.cl.index(self._index, 'type', {},
                                         consistency=1)
            with self.assertRaises(ValueError):
                yield from self.cl.index(self._index, 'type', {},
                                         consistency='1')
            with self.assertRaises(TypeError):
                yield from self.cl.index(self._index, 'type', {},
                                         replication=1)
            with self.assertRaises(ValueError):
                yield from self.cl.index(self._index, 'type', {},
                                         replication='1')
            with self.assertRaises(TypeError):
                yield from self.cl.index(self._index, 'type', {},
                                         op_type=1)
            with self.assertRaises(ValueError):
                yield from self.cl.index(self._index, 'type', {},
                                         op_type='1')
            with self.assertRaises(TypeError):
                yield from self.cl.index(self._index, 'tweet', {},
                                         version_type=1)
            with self.assertRaises(ValueError):
                yield from self.cl.index(self._index, 'tweet', {},
                                         version_type='1')

        self.loop.run_until_complete(go())

    def test_exist(self):
        """ exists """
        @asyncio.coroutine
        def go():
            id = '100'
            # test non-exist
            data = yield from self.cl.exists(self._index, id,
                                             refresh=True,
                                             realtime=True,
                                             preference='_local')
            self.assertFalse(data)
            # test exist
            yield from self.cl.index(self._index, 'exist',
                                     {'user': 'opa', 'tim': 'none'},
                                     id,
                                     routing='opa')
            data = yield from self.cl.exists(self._index, id,
                                             routing='opa')
            self.assertTrue(data)
            data = yield from self.cl.exists(self._index, id, parent='1')
            self.assertFalse(data, data)
        self.loop.run_until_complete(go())

    def test_get(self):
        """ get """
        @asyncio.coroutine
        def go():
            id = '200'
            yield from self.cl.index(self._index, 'test_get', MESSAGES[1], id)
            data = yield from self.cl.get(self._index, id,
                                          realtime=True,
                                          refresh=True)
            self.assertEqual(data['_id'], id)
            self.assertEqual(data['_index'], self._index)
            self.assertEqual(data['_type'], 'test_get')
            self.assertEqual(data['_version'], 1)
            self.assertTrue(data['found'], data)
            self.assertEqual(data['_source'], MESSAGES[1])
            data = yield from self.cl.get(self._index, id,
                                          _source=False)
            self.assertEqual(data['_source'], {})
            data = yield from self.cl.get(self._index, id,
                                          _source_exclude='counter',
                                          _source_include='*')
            self.assertNotIn('counter', data, data)
            data = yield from self.cl.get(self._index, id,
                                          fields='user,skills',
                                          routing='Sidor',
                                          preference='_local',
                                          version=1,
                                          version_type='internal')
            self.assertIn('fields', data, data)
            self.assertIn('user', data['fields'], data)
            self.assertIn('skills', data['fields'], data)
            with self.assertRaises(NotFoundError):
                yield from self.cl.get(self._index, id, parent='1')
            with self.assertRaises(TypeError):
                yield from self.cl.get(self._index, id,
                                       version_type=1)
            with self.assertRaises(ValueError):
                yield from self.cl.get(self._index, id,
                                       version_type='1')

        self.loop.run_until_complete(go())

    def test_get_source(self):
        """ get_source """
        @asyncio.coroutine
        def go():
            yield from self.cl.index(self._index,
                                     'test_get_source',
                                     MESSAGES[0],
                                     '1')
            data = yield from self.cl.get_source(self._index, '1')
            self.assertEqual(data, MESSAGES[0])

            id = '200'
            yield from self.cl.index(
                self._index, 'test_get_source', MESSAGES[2], id,
                routing='Poligrafovich'
                )
            data = yield from self.cl.get_source(self._index, id,
                                                 routing='Poligrafovich',
                                                 preference='_local',
                                                 version=1,
                                                 version_type='internal',
                                                 realtime=True,
                                                 refresh=True)
            self.assertEqual(data, MESSAGES[2])
            data = yield from self.cl.get_source(self._index, id,
                                                 routing='Poligrafovich',
                                                 _source=False)
            self.assertEqual(data, {})
            data = yield from self.cl.get_source(self._index, id,
                                                 routing='Poligrafovich',
                                                 _source_exclude='counter',
                                                 _source_include='*')
            self.assertNotIn('counter', data, data)
            self.assertTrue('user', data)
            with self.assertRaises(NotFoundError):
                yield from self.cl.get_source(self._index, id, parent='1')
            with self.assertRaises(TypeError):
                yield from self.cl.get_source(self._index, id,
                                              version_type=1)
            with self.assertRaises(ValueError):
                yield from self.cl.get_source(self._index, id,
                                              version_type='1')
        self.loop.run_until_complete(go())

    def test_delete(self):
        """ delete """
        @asyncio.coroutine
        def go():
            yield from self.cl.index(self._index, 'testdoc', MESSAGES[2], '1')
            data = yield from self.cl.delete(self._index, 'testdoc', '1')
            self.assertTrue(data['found'], data)
            with self.assertRaises(NotFoundError):
                data = yield from self.cl.delete(self._index, 'testdoc', '1',
                                                 consistency='one',
                                                 replication='async',
                                                 refresh=True,
                                                 version_type='internal',
                                                 version=2,
                                                 timeout=30000,
                                                 routing='test',
                                                 parent='1')
            with self.assertRaises(TypeError):
                yield from self.cl.delete(self._index, 'type', {},
                                          consistency=1)
            with self.assertRaises(ValueError):
                yield from self.cl.delete(self._index, 'type', {},
                                          consistency='1')
            with self.assertRaises(TypeError):
                yield from self.cl.delete(self._index, 'type', {},
                                          replication=1)
            with self.assertRaises(ValueError):
                yield from self.cl.delete(self._index, 'type', {},
                                          replication='1')
            with self.assertRaises(TypeError):
                yield from self.cl.delete(self._index, 'type', {},
                                          version_type=1)
            with self.assertRaises(ValueError):
                yield from self.cl.delete(self._index, 'type', {},
                                          version_type='1')

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
            yield from self.cl.index(self._index, 'testdoc', MESSAGES[2],
                                     '1',
                                     routing='Fedor')
            yield from self.cl.update(self._index, 'testdoc', '1',
                                      script,
                                      version_type='internal',
                                      version=1,
                                      routing='Fedor')
            data = yield from self.cl.get(self._index, '1', routing='Fedor')
            self.assertEqual(data['_source']['counter'], 123)
            self.assertEqual(data['_version'], 2)

            data = yield from self.cl.update(self._index, 'testdoc', '1',
                                             script,
                                             timestamp='2009-11-15T14:12:12',
                                             ttl='1d',
                                             consistency='one',
                                             timeout=30000,
                                             refresh=True,
                                             replication='async',
                                             retry_on_conflict=2,
                                             routing='Fedor',
                                             lang='en')
            self.assertEqual(data['_version'], 3)
            with self.assertRaises(NotFoundError):
                yield from self.cl.update(
                    self._index, 'testdoc', '1',
                    script={},
                    fields='user',
                    parent='1')
            with self.assertRaises(TypeError):
                yield from self.cl.update(self._index, 'type', {},
                                          consistency=1)
            with self.assertRaises(ValueError):
                yield from self.cl.update(self._index, 'type', {},
                                          consistency='1')
            with self.assertRaises(TypeError):
                yield from self.cl.update(self._index, 'type', {},
                                          replication=1)
            with self.assertRaises(ValueError):
                yield from self.cl.update(self._index, 'type', {},
                                          replication='1')
            with self.assertRaises(TypeError):
                yield from self.cl.update(self._index, 'type', {},
                                          version_type=1)
            with self.assertRaises(ValueError):
                yield from self.cl.update(self._index, 'type', {},
                                          version_type='1')

        self.loop.run_until_complete(go())

    def test_search(self):
        """ search """
        @asyncio.coroutine
        def go():
            yield from self.cl.index(self._index, 'testdoc',
                                     MESSAGES[0], '1',
                                     refresh=True)
            yield from self.cl.index(self._index, 'testdoc',
                                     MESSAGES[1], '2',
                                     refresh=True)
            yield from self.cl.index(self._index, 'testdoc',
                                     MESSAGES[2], '3',
                                     refresh=True)
            data = yield from self.cl.search(self._index,
                                             'testdoc',
                                             q='skills:Python',
                                             _source=False,
                                             _source_include='skills')
            self.assertEqual(data['hits']['total'], 2, data)
            self.assertIn('skills', data['hits']['hits'][0]['_source'])
            self.assertIn('skills', data['hits']['hits'][1]['_source'])
            data = yield from self.cl.search(self._index,
                                             'testdoc',
                                             q='skills:Python',
                                             _source_exclude='skills',
                                             analyzer='standard',
                                             default_operator='AND',
                                             analyze_wildcard=True,
                                             version=2,
                                             timeout=30000,
                                             allow_no_indices=True,
                                             ignore_unavailable=True,
                                             df='_all',
                                             explain=True,
                                             fields='skills,user',
                                             from_=0,
                                             expand_wildcards='open',
                                             lenient=True,
                                             lowercase_expanded_terms=True,
                                             preference='random',
                                             scroll='1s',
                                             search_type='query_then_fetch',
                                             size=100,
                                             sort='user:true',
                                             stats=True
                                             )
            self.assertNotIn('skills', data['hits']['hits'][0]['_source'])
            self.assertNotIn('skills', data['hits']['hits'][1]['_source'])
            with self.assertRaises(TypeError):
                yield from self.cl.search(default_operator=1,
                                          indices_boost=False)
            with self.assertRaises(ValueError):
                yield from self.cl.search(doc_type='testdoc',
                                          q='skills:Python',
                                          routing='Sidor',
                                          source='Query DSL',
                                          suggest_field='user',
                                          suggest_text='test',
                                          suggest_mode='missing',
                                          suggest_size=100,
                                          default_operator='1')

            with self.assertRaises(TypeError):
                yield from self.cl.search(self._index,
                                          'testdoc',
                                          q='skills:Python',
                                          suggest_mode=1)
            with self.assertRaises(ValueError):
                yield from self.cl.search(self._index,
                                          'testdoc',
                                          q='skills:Python',
                                          suggest_mode='1')

            with self.assertRaises(TypeError):
                yield from self.cl.search(self._index,
                                          'testdoc',
                                          q='skills:Python',
                                          search_type=1)
            with self.assertRaises(ValueError):
                yield from self.cl.search(self._index,
                                          'testdoc',
                                          q='skills:Python',
                                          search_type='1')

            with self.assertRaises(TypeError):
                yield from self.cl.search(self._index,
                                          'testdoc',
                                          q='skills:Python',
                                          expand_wildcards=1)
            with self.assertRaises(ValueError):
                yield from self.cl.search(self._index,
                                          'testdoc',
                                          q='skills:Python',
                                          expand_wildcards='1')
        self.loop.run_until_complete(go())

    def test_count(self):
        """ count """
        @asyncio.coroutine
        def go():
            yield from self.cl.index(self._index, 'testdoc',
                                     MESSAGES[0], '1',
                                     refresh=True)
            yield from self.cl.index(self._index, 'testdoc',
                                     MESSAGES[1], '2',
                                     refresh=True)
            yield from self.cl.index(self._index, 'testdoc',
                                     MESSAGES[2], '3',
                                     refresh=True)
            data = yield from self.cl.count(
                self._index, 'testdoc', q='skills:Python')
            self.assertEqual(data['count'], 2, data)
            data = yield from self.cl.count(
                self._index, 'testdoc', q='skills:Python',
                ignore_unavailable=True,
                expand_wildcards='open',
                allow_no_indices=False,
                min_score=1,
                preference='random')
            self.assertEqual(data['count'], 2, data)

            with self.assertRaises(TypeError):
                yield from self.cl.count(
                    self._index, 'testdoc',
                    expand_wildcards=1)

            with self.assertRaises(ValueError):
                yield from self.cl.count(
                    self._index, 'testdoc', q='skills:Python',
                    expand_wildcards='1',
                    routing='Sidor',
                    source='Query DSL')

        self.loop.run_until_complete(go())

    def test_explain(self):
        """ explain """
        @asyncio.coroutine
        def go():
            yield from self.cl.index(self._index, 'testdoc',
                                     MESSAGES[0], '1',
                                     refresh=True)
            yield from self.cl.index(self._index, 'testdoc',
                                     MESSAGES[1], '2',
                                     refresh=True)
            yield from self.cl.index(self._index, 'testdoc',
                                     MESSAGES[2], '3',
                                     refresh=True)

            data = yield from self.cl.explain(
                self._index, 'testdoc', '3',
                q='skills:Python')
            self.assertTrue(data['matched'], data)
            data = yield from self.cl.explain(
                self._index, 'testdoc', '1',
                q='skills:Python',
                analyze_wildcard=True,
                _source=False,
                _source_include='user',
                _source_exclude='counter',
                analyzer='standard',
                default_operator='and',
                df='_all',
                fields='user,counter',
                lenient=True,
                lowercase_expanded_terms=False,
                preference='random')
            self.assertTrue(data['matched'], data)

            with self.assertRaises(TypeError):
                yield from self.cl.explain(
                    self._index, 'testdoc', '1',
                    q='skills:Python',
                    default_operator=1)
            with self.assertRaises(ValueError):
                yield from self.cl.explain(
                    self._index, 'testdoc', '1',
                    default_operator='1',
                    parent='2',
                    routing='Sidor',
                    source='DSL Query')

        self.loop.run_until_complete(go())

    def test_delete_by_query(self):
        """ delete_by_query """
        DQ = {"query": {"term": {"user": "Fedor Poligrafovich"}}}

        @asyncio.coroutine
        def go():
            yield from self.cl.index(self._index, 'testdoc', MESSAGES[3], '1')
            yield from self.cl.index(self._index, 'testdoc', MESSAGES[2], '2')
            # data = yield from self.cl.delete(self._index, 'testdoc', '1')
            # self.assertTrue(data['found'], data)

            data = yield from self.cl.delete_by_query(
                self._index,
                'testdoc',
                q='user:Fedor Poligrafovich'
            )
            self.assertIn('_indices', data, data)
            with self.assertRaises(TransportError):
                yield from self.cl.delete_by_query(
                    body=DQ,
                    allow_no_indices=True,
                    analyzer='standard',
                    df='_all',
                    expand_wildcards='open',
                    consistency='all',
                    default_operator='AND',
                    ignore_unavailable=True,
                    replication='async',
                    routing='Fedor',
                    source='',
                    timeout='100ms')
            with self.assertRaises(TypeError):
                yield from self.cl.delete_by_query(default_operator=1)
            with self.assertRaises(ValueError):
                yield from self.cl.delete_by_query(default_operator='1')
            with self.assertRaises(TypeError):
                yield from self.cl.delete_by_query(consistency=1)
            with self.assertRaises(ValueError):
                yield from self.cl.delete_by_query(consistency='1')
            with self.assertRaises(TypeError):
                yield from self.cl.delete_by_query(replication=1)
            with self.assertRaises(ValueError):
                yield from self.cl.delete_by_query(replication='1')
            with self.assertRaises(TypeError):
                yield from self.cl.delete_by_query(expand_wildcards=1)
            with self.assertRaises(ValueError):
                yield from self.cl.delete_by_query(expand_wildcards='1')
        self.loop.run_until_complete(go())

    def test_msearch(self):
        """ msearch """
        queries = [
            {"_index": self._index},
            {"query": {"match_all": {}}, "from": 0, "size": 10},
            {"_index": self._index},
            {"query": {"match_all": {}}}
        ]

        @asyncio.coroutine
        def go():
            yield from self.cl.index(self._index, 'testdoc',
                                     MESSAGES[0], '1',
                                     refresh=True)
            yield from self.cl.index(self._index, 'testdoc',
                                     MESSAGES[1], '2',
                                     refresh=True)
            yield from self.cl.index(self._index, 'testdoc',
                                     MESSAGES[2], '3',
                                     refresh=True)

            data = yield from self.cl.msearch(queries)
            self.assertGreater(len(data['responses']), 0, data)
            data = yield from self.cl.msearch(queries, search_type='count')
            self.assertGreater(len(data['responses']), 0, data)
            with self.assertRaises(TypeError):
                yield from self.cl.msearch(queries, search_type=1)
            with self.assertRaises(ValueError):
                yield from self.cl.msearch(queries, search_type='1')

        self.loop.run_until_complete(go())

    def test_scroll(self):
        """ scroll """
        @asyncio.coroutine
        def go():
            pass
            # scroll_id = 'c2Nhbjs2OzMFXNlNyNm5JWUc1'
            # with self.assertRaises(RequestError):
            #     yield from self.cl.scroll(scroll_id,
            #                               scroll='1m')
            # with self.assertRaises(RequestError):
            #     yield from self.cl.scroll(scroll_id)

        self.loop.run_until_complete(go())

    def test_clear_scroll(self):
        """ clear_scroll """
        @asyncio.coroutine
        def go():
            pass
            # scroll_id = 'c2Nhbjs2OzMFXNlNyNm5JWUc1'
            # yield from self.cl.scroll(scroll_id)
            # yield from self.cl.clear_scroll(scroll_id)

        self.loop.run_until_complete(go())

    def test_bulk(self):
        bulks = [
            {"index": {"_index": self._index, "_type": "type1", "_id": "1"}},
            {"name": "hiq", "age": 10},
            {"index": {"_index": self._index, "_type": "type1", "_id": "2"}},
            {"name": "hiq", "age": 10},
            {"index": {"_index": self._index, "_type": "type1", "_id": "3"}},
            {"name": "hiq", "age": 10}
        ]

        @asyncio.coroutine
        def go():
            data = yield from self.cl.bulk(bulks)
            self.assertFalse(data['errors'])
            self.assertEqual(3, len(data['items']), data)
            data = yield from self.cl.bulk(
                bulks,
                consistency='one',
                refresh=True,
                routing='hiq',
                replication='async',
                timeout='1s'
            )
            with self.assertRaises(TypeError):
                yield from self.cl.bulk(bulks, consistency=1)
            with self.assertRaises(ValueError):
                yield from self.cl.bulk(bulks, consistency='1')
            with self.assertRaises(TypeError):
                yield from self.cl.bulk(bulks, replication=1)
            with self.assertRaises(ValueError):
                yield from self.cl.bulk(bulks, replication='1')
        self.loop.run_until_complete(go())

    def test_mget(self):
        """ mget """
        @asyncio.coroutine
        def go():
            yield from self.cl.index(
                self._index, 'testdoc', MESSAGES[0], '1', refresh=True)
            yield from self.cl.index(
                self._index, 'testdoc', MESSAGES[1], '2', refresh=True)
            yield from self.cl.index(
                self._index, 'testdoc', MESSAGES[2], '3', refresh=True)
            body = {
                "docs": [
                    {"_index": self._index, "_type": "testdoc", "_id": "1"},
                    {"_index": self._index, "_type": "testdoc", "_id": "2"}
                ]
            }
            data = yield from self.cl.mget(body)
            self.assertEqual(len(data['docs']), 2)
            data = yield from self.cl.mget(
                body,
                _source_exclude='birthDate',
                _source_include='user,skills',
                _source=False,
                fields='user,skills',
                realtime=True,
                refresh=True,
                preference='random',
                parent=''
            )
            self.assertIn('skills', data['docs'][0]['fields'], data)
            self.assertIn('user', data['docs'][0]['fields'], data)
            self.assertIn('skills', data['docs'][0]['_source'], data)
            self.assertIn('user', data['docs'][0]['_source'], data)
            yield from self.cl.mget(body, routing='Sidor')

        self.loop.run_until_complete(go())

    def test_suggest(self):
        """ search """
        @asyncio.coroutine
        def go():
            mapping = {
                "testdoc": {
                    "properties": {
                        "birthDate": {
                            "type": "date",
                            "format": "dateOptionalTime"
                        },
                        "counter": {
                            "type": "long"
                        },
                        # this one is different
                        "message": {
                            "type": "completion"
                        },
                        "skills": {
                            "type": "string"
                        },
                        "user": {
                            "type": "string"
                        }
                    }
                }
            }

            yield from self.cl.indices.create(self._index)
            yield from self.cl.indices.put_mapping(
                self._index,
                'testdoc',
                mapping,
            )
            yield from self.cl.index(self._index, 'testdoc',
                                     MESSAGES[0], '1',
                                     refresh=True)
            yield from self.cl.index(self._index, 'testdoc',
                                     MESSAGES[1], '2',
                                     refresh=True)
            b = {
                "my-suggestion": {
                    "text": "trying out",
                    "completion": {
                        "field": "message"
                    }
                }
            }

            data = yield from self.cl.suggest(
                self._index,
                body=b,
            )
            results = data['my-suggestion'][0]['options']
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]['text'], 'trying out Elasticsearch')

        self.loop.run_until_complete(go())

    def test_percolate(self):
        @asyncio.coroutine
        def go():
            mapping = {
                "testdoc": {
                    "properties": {
                        "message": {
                            "type": "string"
                        }
                    }
                }
            }
            yield from self.cl.indices.create(self._index)
            yield from self.cl.indices.put_mapping(
                self._index,
                'testdoc',
                mapping,
            )

            percolator = {
                "query": {
                    "match": {
                        "message": "bonsai tree"
                    }
                }
            }
            # register percolator
            yield from self.cl.index(self._index, '.percolator',
                                     percolator, '1',
                                     refresh=True)

            b = {
                "doc": {
                    "message": "A new bonsai tree in the office"
                }
            }
            # percolate a doc from b
            data = yield from self.cl.percolate(
                self._index,
                'testdoc',
                body=b,
            )
            self.assertEqual(data['total'], 1)
            self.assertEqual(
                data['matches'][0],
                {'_index': 'test_elasticsearch', '_id': '1'}
            )

            # percolate_count gives only count, no matches
            data = yield from self.cl.count_percolate(
                self._index,
                'testdoc',
                body=b,
            )

            self.assertEqual(data['total'], 1)
            self.assertTrue('matches' not in data)

        self.loop.run_until_complete(go())

    def test_mpercolate(self):
        @asyncio.coroutine
        def go():
            mapping = {
                "testdoc": {
                    "properties": {
                        "message": {
                            "type": "string"
                        }
                    }
                }
            }
            yield from self.cl.indices.create(self._index)
            yield from self.cl.indices.put_mapping(
                self._index,
                'testdoc',
                mapping,
            )

            percolator = {
                "query": {
                    "match": {
                        "message": "bonsai tree"
                    }
                }
            }
            # register percolator
            yield from self.cl.index(self._index, '.percolator',
                                     percolator, '1',
                                     refresh=True)

            body = [
                {
                    'percolate': {
                        'index': self._index,
                        'type': 'testdoc',
                    }
                },
                {
                    "doc": {
                        "message": "A new bonsai tree in the office"
                    }
                }
            ]

            data = yield from self.cl.mpercolate(
                body,
                self._index,
                'testdoc',
            )

            self.assertEqual(len(data['responses']), 1)
            item = data['responses'][0]
            self.assertEqual(item['total'], 1)
            self.assertEqual(
                item['matches'][0],
                {'_index': 'test_elasticsearch', '_id': '1'}
            )

        self.loop.run_until_complete(go())

    def test_termvector(self):
        @asyncio.coroutine
        def go():
            mapping = {
                "testdoc": {
                    "properties": {
                        "message": {
                            "type": "string",
                            "term_vector": "with_positions_offsets_payloads",
                            "store": True,
                        }
                    }
                }
            }
            yield from self.cl.indices.create(self._index)
            yield from self.cl.indices.put_mapping(
                self._index,
                'testdoc',
                mapping,
            )

            doc = {
                'message': 'Hello world',
            }

            yield from self.cl.index(self._index, 'testdoc',
                                     doc, '1',
                                     refresh=True)

            data = yield from self.cl.termvector(self._index, 'testdoc', '1')

            vector_data = data['term_vectors']['message']
            self.assertEqual(vector_data['field_statistics'], {
                "sum_doc_freq": 2,
                "doc_count": 1,
                "sum_ttf": 2
            })
            self.assertTrue('hello' in vector_data['terms'])
            self.assertTrue('world' in vector_data['terms'])

        self.loop.run_until_complete(go())

    def test_mtermvectors(self):
        @asyncio.coroutine
        def go():
            mapping = {
                "testdoc": {
                    "properties": {
                        "message": {
                            "type": "string",
                            "term_vector": "with_positions_offsets_payloads",
                            "store": True,
                        }
                    }
                }
            }
            yield from self.cl.indices.create(self._index)
            yield from self.cl.indices.put_mapping(
                self._index,
                'testdoc',
                mapping,
            )

            doc = {
                'message': 'Hello world',
            }

            yield from self.cl.index(self._index, 'testdoc',
                                     doc, '1',
                                     refresh=True)
            doc = {
                'message': 'Second term',
            }

            yield from self.cl.index(self._index, 'testdoc',
                                     doc, '2',
                                     refresh=True)

            data = yield from self.cl.mtermvectors(
                self._index, 'testdoc', ids='1,2'
            )

            self.assertEqual(len(data['docs']), 2)
            self.assertTrue('term_vectors' in data['docs'][0])
            self.assertTrue('term_vectors' in data['docs'][1])

        self.loop.run_until_complete(go())

    def test_scripts_management(self):
        @asyncio.coroutine
        def go():
            script = {'script': 'log(_score * 2)'}

            # adding
            yield from self.cl.put_script('groovy', 'test_script', script)

            # getting and checking
            got_script = yield from self.cl.get_script('groovy', 'test_script')
            self.assertEqual(script['script'], got_script['script'])

            # deleting
            yield from self.cl.delete_script('groovy', 'test_script')
            with self.assertRaises(NotFoundError):
                got_script = yield from self.cl.get_script(
                    'groovy', 'test_script'
                )

        self.loop.run_until_complete(go())

    def test_scripts_execution(self):
        @asyncio.coroutine
        def go():
            script = {
                'script': '2*val',
            }
            query = {
                "query": {
                    "match": {
                        "user": "Johny Mnemonic"
                    }
                },
                "script_fields": {
                    "test1": {
                        "lang": "groovy",
                        "script_id": "calculate-score",
                        "params": {
                            "val": 2,
                        }
                    }
                }
            }

            yield from self.cl.index(self._index, 'testdoc',
                                     MESSAGES[0], '1',
                                     refresh=True)

            yield from self.cl.put_script('groovy', 'calculate-score', script)
            data = yield from self.cl.search(self._index, 'testdoc', query)
            res = data['hits']['hits'][0]['fields']['test1'][0]
            self.assertEqual(res, 4)  # 2*2

        self.loop.run_until_complete(go())

    def test_templates_management(self):
        @asyncio.coroutine
        def go():
            template = {
                "template": {
                    "query": {
                        "match": {
                            "user": "{{query_string}}"
                        }
                    }
                }
            }

            yield from self.cl.put_template('test_template', template)

            data = yield from self.cl.get_template('test_template')
            self.assertTrue(template, data)

            yield from self.cl.delete_template('test_template')
            with self.assertRaises(NotFoundError):
                yield from self.cl.get_template('test_template')

        self.loop.run_until_complete(go())

    def test_template_search(self):
        @asyncio.coroutine
        def go():
            template = {
                "template": {
                    "query": {
                        "match": {
                            "user": "{{query_string}}"
                        }
                    }
                }
            }
            search_body = {
                "template": {
                    "id": "test_template"
                },
                "params": {
                    "query_string": "Johny Mnemonic"
                }
            }
            yield from self.cl.index(
                self._index, 'testdoc', MESSAGES[0], '1',
                refresh=True
            )

            yield from self.cl.put_template('test_template', template)

            data = yield from self.cl.search_template(
                self._index, 'testdoc', body=search_body
            )
            self.assertEqual(data['hits']['total'], 1)

        self.loop.run_until_complete(go())

    def test_search_shards(self):
        @asyncio.coroutine
        def go():
            yield from self.cl.index(
                self._index, 'testdoc', MESSAGES[0], '1',
                refresh=True
            )
            data = yield from self.cl.search_shards(
                self._index, 'testdoc'
            )
            self.assertTrue('nodes' in data)
            self.assertTrue(len(data['nodes']) > 0)
            self.assertTrue('shards' in data)
            self.assertTrue(len(data['shards']) > 0)

        self.loop.run_until_complete(go())

    def test_mlt(self):
        @asyncio.coroutine
        def go():
            msg = MESSAGES[0].copy()
            # mlt needs quite a lot of text to work
            msg['message'] = '''
            Additionally, More Like This can find documents that are "like"
            a set of chosen documents. The syntax to specify one or more
            documents is similar to the Multi GET API, and supports the
            ids or docs array. If only one document is specified,
            the query behaves the same as the More Like This API.'''
            # and quite a lot of documents
            for i in range(50):
                yield from self.cl.index(
                    self._index, 'testdoc', msg, str(i),
                    refresh=True
                )

            data = yield from self.cl.mlt(
                self._index, 'testdoc', '1'
            )
            # initial document is not included
            self.assertEqual(data['hits']['total'], 49)
            self.assertEqual(data['hits']['hits'][0]['_source'], msg)

        self.loop.run_until_complete(go())

    # def test_(self):
    #     @asyncio.coroutine
    #     def go():
    #         pass
    #     self.loop.run_until_complete(go())
