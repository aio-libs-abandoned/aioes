import asyncio
import unittest
from aioes import Elasticsearch
from aioes.exception import (NotFoundError, ConflictError,
                             RequestError)

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

    def test_ping(self):
        """ ping """
        @asyncio.coroutine
        def go():
            data = yield from self.cl.ping()
            self.assertTrue(data)
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
                                            timeout='5m',
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
                                                 timeout='1s',
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
                                             timeout='5m',
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
                                             timeout='1s',
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
            # import ipdb; ipdb.set_trace()
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

        self.loop.run_until_complete(go())

#    def test_mget(self):
#        """ mget """
#        @asyncio.coroutine
#        def go():
#            body = {"ids": ['200', '2']}
#            yield from self.cl.index(
#                             self._index, 'test_mget', MESSAGES[0], '200')
#            data = yield from self.cl.mget(body, index=self._index)
#            import ipdb; ipdb.set_trace()
#        self.loop.run_until_complete(go())

    # def test_(self):
    #     @asyncio.coroutine
    #     def go():
    #         pass
    #     self.loop.run_until_complete(go())
