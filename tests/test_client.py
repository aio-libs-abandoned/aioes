import asyncio
import pytest
from aioes import Elasticsearch
from aioes.exception import (NotFoundError, RequestError,
                             TransportError)

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


@pytest.fixture
def index():
    return 'test_elasticsearch'


@pytest.fixture
def client(es_params, index, loop):
    client = Elasticsearch([{'host': es_params['host']}], loop=loop)
    try:
        loop.run_until_complete(client.delete(index, '', ''))
    except NotFoundError:
        pass
    yield client
    client.close()


@asyncio.coroutine
def test_ping(client):
    """ ping """

    class R:
        @asyncio.coroutine
        def perform_request(self, a, b):
            yield
            raise TransportError

        def close(self):
            pass

    data = yield from client.ping()
    assert data
    client._transport = R()
    yield from client.ping()


@asyncio.coroutine
def test_info(client):
    """ test_info """
    data = yield from client.info()
    assert data['cluster_name'] == 'elasticsearch'


@asyncio.coroutine
def test_create(client, index):
    """ create index """
    data = yield from client.create(
        index, 'tweet',
        {
            'user': 'Bob',
            'skills': ['C', 'Python', 'Assembler'],
            'date': '2009-11-15T14:12:12'
        },
        '1',
        routing='Bob')
    assert data['_index'] == index
    assert data['_type'] == 'tweet'
    assert data['_version'] == 1
    assert data['created']
    # test for conflict (BROKEN)
    # with pytest.raises(ConflictError):
    #     yield from client.create(index, 'tweet', {}, '1')


@asyncio.coroutine
def test_index(client, index):
    """ auto-create index """
    data = yield from client.index(index, 'tweet', {}, '1')
    assert data['_index'] == index
    assert data['_type'] == 'tweet'
    assert data['_id'] == '1'
    assert data['_version'] == 1
    assert data['created']
    # test increment version
    data = yield from client.index(index, 'tweet', {}, '1')
    assert data['_version'] == 2
    assert not data['created']
    # test 'external' version_type
    data = yield from client.index(index, 'tweet', {}, '12',
                                   version_type='external',
                                   version=122,
                                   timestamp='2009-11-15T14:12:12',
                                   ttl='1d',
                                   consistency='one',
                                   timeout='5m',
                                   refresh=True,
                                   replication='async')
    assert data['_version'] == 122
    assert data['created']
    with pytest.raises(RequestError):
        yield from client.index(index, 'type', {},
                                parent='1',
                                percolate='')
    with pytest.raises(TypeError):
        yield from client.index(index, 'type', {},
                                consistency=1)
    with pytest.raises(ValueError):
        yield from client.index(index, 'type', {},
                                consistency='1')
    with pytest.raises(TypeError):
        yield from client.index(index, 'type', {},
                                replication=1)
    with pytest.raises(ValueError):
        yield from client.index(index, 'type', {},
                                replication='1')
    with pytest.raises(TypeError):
        yield from client.index(index, 'type', {},
                                op_type=1)
    with pytest.raises(ValueError):
        yield from client.index(index, 'type', {},
                                op_type='1')
    with pytest.raises(TypeError):
        yield from client.index(index, 'tweet', {},
                                version_type=1)
    with pytest.raises(ValueError):
        yield from client.index(index, 'tweet', {},
                                version_type='1')


@asyncio.coroutine
def test_exist(client, index):
    """ exists """
    id = '100'
    # test non-exist
    data = yield from client.exists(index, id,
                                    refresh=True,
                                    realtime=True,
                                    preference='_local')
    assert not data
    # test exist
    yield from client.index(index, 'exist',
                            {'user': 'opa', 'tim': 'none'},
                            id,
                            routing='opa')
    data = yield from client.exists(index, id,
                                    routing='opa')
    assert data
    data = yield from client.exists(index, id, parent='1')
    assert not data


@asyncio.coroutine
def test_get(client, index):
    """ get """
    id = '200'
    yield from client.index(index, 'test_get', MESSAGES[1], id)
    data = yield from client.get(index, id,
                                 realtime=True,
                                 refresh=True)
    assert data['_id'] == id
    assert data['_index'] == index
    assert data['_type'] == 'test_get'
    assert data['_version'] == 1
    assert data['found']
    assert data['_source'] == MESSAGES[1]
    data = yield from client.get(index, id,
                                 _source=False)
    assert '_source' not in data
    data = yield from client.get(index, id,
                                 _source_exclude='counter',
                                 _source_include='*')
    assert 'counter' not in data
    with pytest.raises(NotFoundError):
        yield from client.get(index, id, parent='1')
    with pytest.raises(TypeError):
        yield from client.get(index, id,
                              version_type=1)
    with pytest.raises(ValueError):
        yield from client.get(index, id,
                              version_type='1')


@asyncio.coroutine
def test_get_source(client, index):
    """ get_source """
    yield from client.index(index,
                            'test_get_source',
                            MESSAGES[0],
                            '1')
    data = yield from client.get_source(index, '1')
    assert data == MESSAGES[0]

    id = '200'
    yield from client.index(
        index, 'test_get_source', MESSAGES[2], id,
        routing='Poligrafovich'
        )
    data = yield from client.get_source(index, id,
                                        routing='Poligrafovich',
                                        preference='_local',
                                        version=1,
                                        version_type='internal',
                                        realtime=True,
                                        refresh=True)
    assert data == MESSAGES[2]
    data = yield from client.get_source(index, id,
                                        routing='Poligrafovich',
                                        _source_exclude='counter',
                                        _source_include='*')
    assert 'counter' not in data
    with pytest.raises(NotFoundError):
        yield from client.get_source(index, id, parent='1')
    with pytest.raises(TypeError):
        yield from client.get_source(index, id,
                                     version_type=1)
    with pytest.raises(ValueError):
        yield from client.get_source(index, id,
                                     version_type='1')


@asyncio.coroutine
def test_delete(client, index):
    """ delete """
    yield from client.index(index, 'testdoc', MESSAGES[2], '1')
    data = yield from client.delete(index, 'testdoc', '1')
    assert data['found']
    with pytest.raises(NotFoundError):
        data = yield from client.delete(index, 'testdoc', '1',
                                        consistency='one',
                                        replication='async',
                                        refresh=True,
                                        timeout='5m',
                                        routing='test',
                                        parent='1')
    with pytest.raises(TypeError):
        yield from client.delete(index, 'type', {},
                                 consistency=1)
    with pytest.raises(ValueError):
        yield from client.delete(index, 'type', {},
                                 consistency='1')
    with pytest.raises(TypeError):
        yield from client.delete(index, 'type', {},
                                 replication=1)
    with pytest.raises(ValueError):
        yield from client.delete(index, 'type', {},
                                 replication='1')
    with pytest.raises(TypeError):
        yield from client.delete(index, 'type', {},
                                 version_type=1)
    with pytest.raises(ValueError):
        yield from client.delete(index, 'type', {},
                                 version_type='1')


@asyncio.coroutine
def test_update(client, index):
    """ update """
    script = {
        "doc": {
            "counter": 123
        }
    }
    yield from client.index(index, 'testdoc', MESSAGES[2],
                            '1',
                            routing='Fedor')
    yield from client.update(index, 'testdoc', '1',
                             script,
                             version_type='internal',
                             version=1,
                             routing='Fedor')
    data = yield from client.get(index, '1', routing='Fedor')
    assert data['_source']['counter'] == 123
    assert data['_version'] == 2

    data = yield from client.update(index, 'testdoc', '1',
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
    with pytest.raises(NotFoundError):
        yield from client.update(
            index, 'testdoc', '1',
            script='{}',
            fields='user',
            parent='1')
    with pytest.raises(TypeError):
        yield from client.update(index, 'type', {},
                                 consistency=1)
    with pytest.raises(ValueError):
        yield from client.update(index, 'type', {},
                                 consistency='1')
    with pytest.raises(TypeError):
        yield from client.update(index, 'type', {},
                                 replication=1)
    with pytest.raises(ValueError):
        yield from client.update(index, 'type', {},
                                 replication='1')
    with pytest.raises(TypeError):
        yield from client.update(index, 'type', {},
                                 version_type=1)
    with pytest.raises(ValueError):
        yield from client.update(index, 'type', {},
                                 version_type='1')


@asyncio.coroutine
def test_search(client, index):
    """ search """
    yield from client.index(index, 'testdoc',
                            MESSAGES[0], '1',
                            refresh=True)
    yield from client.index(index, 'testdoc',
                            MESSAGES[1], '2',
                            refresh=True)
    yield from client.index(index, 'testdoc',
                            MESSAGES[2], '3',
                            refresh=True)
    data = yield from client.search(index,
                                    'testdoc',
                                    q='skills:Python')
    assert data['hits']['total'] == 2
    assert 'skills' in data['hits']['hits'][0]['_source']
    assert 'skills' in data['hits']['hits'][1]['_source']
    data = yield from client.search(index,
                                    'testdoc',
                                    q='skills:Python',
                                    _source_exclude='skills',
                                    analyzer='standard',
                                    default_operator='AND',
                                    analyze_wildcard=True,
                                    version=2,
                                    timeout='5m',
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
                                    stats=True)
    assert 'skills' not in data['hits']['hits'][0]['_source']
    assert 'skills' not in data['hits']['hits'][1]['_source']
    with pytest.raises(TypeError):
        yield from client.search(default_operator=1,
                                 indices_boost=False)
    with pytest.raises(ValueError):
        yield from client.search(doc_type='testdoc',
                                 q='skills:Python',
                                 routing='Sidor',
                                 source='Query DSL',
                                 suggest_field='user',
                                 suggest_text='test',
                                 suggest_mode='missing',
                                 suggest_size=100,
                                 default_operator='1')

    with pytest.raises(TypeError):
        yield from client.search(index,
                                 'testdoc',
                                 q='skills:Python',
                                 suggest_mode=1)
    with pytest.raises(ValueError):
        yield from client.search(index,
                                 'testdoc',
                                 q='skills:Python',
                                 suggest_mode='1')

    with pytest.raises(TypeError):
        yield from client.search(index,
                                 'testdoc',
                                 q='skills:Python',
                                 search_type=1)
    with pytest.raises(ValueError):
        yield from client.search(index,
                                 'testdoc',
                                 q='skills:Python',
                                 search_type='1')

    with pytest.raises(TypeError):
        yield from client.search(index,
                                 'testdoc',
                                 q='skills:Python',
                                 expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.search(index,
                                 'testdoc',
                                 q='skills:Python',
                                 expand_wildcards='1')


@asyncio.coroutine
def test_count(client, index):
    """ count """
    yield from client.index(index, 'testdoc',
                            MESSAGES[0], '1',
                            refresh=True)
    yield from client.index(index, 'testdoc',
                            MESSAGES[1], '2',
                            refresh=True)
    yield from client.index(index, 'testdoc',
                            MESSAGES[2], '3',
                            refresh=True)
    data = yield from client.count(
        index, 'testdoc', q='skills:Python')
    assert data['count'] == 2
    data = yield from client.count(
        index, 'testdoc', q='skills:Python',
        ignore_unavailable=True,
        expand_wildcards='open',
        allow_no_indices=False,
        min_score=1,
        preference='random')
    assert data['count'] == 0

    with pytest.raises(TypeError):
        yield from client.count(
            index, 'testdoc',
            expand_wildcards=1)

    with pytest.raises(ValueError):
        yield from client.count(
            index, 'testdoc', q='skills:Python',
            expand_wildcards='1',
            routing='Sidor',
            source='Query DSL')


@asyncio.coroutine
def test_explain(client, index):
    """ explain """
    yield from client.index(index, 'testdoc',
                            MESSAGES[0], '1',
                            refresh=True)
    yield from client.index(index, 'testdoc',
                            MESSAGES[1], '2',
                            refresh=True)
    yield from client.index(index, 'testdoc',
                            MESSAGES[2], '3',
                            refresh=True)

    data = yield from client.explain(
        index, 'testdoc', '3',
        q='skills:Python')
    assert data['matched']
    data = yield from client.explain(
        index, 'testdoc', '1',
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
    assert data['matched']

    with pytest.raises(TypeError):
        yield from client.explain(
            index, 'testdoc', '1',
            q='skills:Python',
            default_operator=1)
    with pytest.raises(ValueError):
        yield from client.explain(
            index, 'testdoc', '1',
            default_operator='1',
            parent='2',
            routing='Sidor',
            source='DSL Query')


@pytest.mark.xfail
@asyncio.coroutine
def test_delete_by_query(client, index):
    """ delete_by_query """
    DQ = {"query": {"term": {"user": "Fedor Poligrafovich"}}}

    yield from client.index(index, 'testdoc', MESSAGES[3], '1')
    yield from client.index(index, 'testdoc', MESSAGES[2], '2')
    # data = yield from client.delete(index, 'testdoc', '1')
    # self.assertTrue(data['found'], data)

    data = yield from client.delete_by_query(
        index,
        'testdoc',
        q='user:Fedor Poligrafovich'
    )
    assert '_indices' in data
    with pytest.raises(TransportError):
        yield from client.delete_by_query(
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
    with pytest.raises(TypeError):
        yield from client.delete_by_query(default_operator=1)
    with pytest.raises(ValueError):
        yield from client.delete_by_query(default_operator='1')
    with pytest.raises(TypeError):
        yield from client.delete_by_query(consistency=1)
    with pytest.raises(ValueError):
        yield from client.delete_by_query(consistency='1')
    with pytest.raises(TypeError):
        yield from client.delete_by_query(replication=1)
    with pytest.raises(ValueError):
        yield from client.delete_by_query(replication='1')
    with pytest.raises(TypeError):
        yield from client.delete_by_query(expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.delete_by_query(expand_wildcards='1')


@asyncio.coroutine
def test_msearch(client, index):
    """ msearch """
    queries = [
        {"_index": index},
        {"query": {"match_all": {}}, "from": 0, "size": 10},
        {"_index": index},
        {"query": {"match_all": {}}}
    ]

    yield from client.index(index, 'testdoc',
                            MESSAGES[0], '1',
                            refresh=True)
    yield from client.index(index, 'testdoc',
                            MESSAGES[1], '2',
                            refresh=True)
    yield from client.index(index, 'testdoc',
                            MESSAGES[2], '3',
                            refresh=True)

    data = yield from client.msearch(queries)
    assert len(data['responses']) > 0
    data = yield from client.msearch(queries, search_type='count')
    assert len(data['responses']) > 0
    with pytest.raises(TypeError):
        yield from client.msearch(queries, search_type=1)
    with pytest.raises(ValueError):
        yield from client.msearch(queries, search_type='1')


@asyncio.coroutine
def test_bulk(client, index):
    bulks = [
        {"index": {"_index": index, "_type": "type1", "_id": "1"}},
        {"name": "hiq", "age": 10},
        {"index": {"_index": index, "_type": "type1", "_id": "2"}},
        {"name": "hiq", "age": 10},
        {"index": {"_index": index, "_type": "type1", "_id": "3"}},
        {"name": "hiq", "age": 10}
    ]

    data = yield from client.bulk(bulks)
    assert not data['errors']
    assert 3 == len(data['items'])
    data = yield from client.bulk(
        bulks,
        consistency='one',
        refresh=True,
        routing='hiq',
        replication='async',
        timeout='1s'
    )
    with pytest.raises(TypeError):
        yield from client.bulk(bulks, consistency=1)
    with pytest.raises(ValueError):
        yield from client.bulk(bulks, consistency='1')
    with pytest.raises(TypeError):
        yield from client.bulk(bulks, replication=1)
    with pytest.raises(ValueError):
        yield from client.bulk(bulks, replication='1')

    def test_mget(self):
        """ mget """
        @asyncio.coroutine
        def go():
            yield from client.index(
                index, 'testdoc', MESSAGES[0], '1', refresh=True)
            yield from client.index(
                index, 'testdoc', MESSAGES[1], '2', refresh=True)
            yield from client.index(
                index, 'testdoc', MESSAGES[2], '3', refresh=True)
            body = {
                "docs": [
                    {"_index": index, "_type": "testdoc", "_id": "1"},
                    {"_index": index, "_type": "testdoc", "_id": "2"}
                ]
            }
            data = yield from client.mget(body)
            self.assertEqual(len(data['docs']), 2)
            data = yield from client.mget(
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
            yield from client.mget(body, routing='Sidor')

        self.loop.run_until_complete(go())


@asyncio.coroutine
def test_suggest(client, index):
    """ search """
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

    yield from client.indices.create(index)
    yield from client.indices.put_mapping(
        index,
        'testdoc',
        mapping,
    )
    yield from client.index(index, 'testdoc',
                            MESSAGES[0], '1',
                            refresh=True)
    yield from client.index(index, 'testdoc',
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

    data = yield from client.suggest(
        index,
        body=b,
    )
    results = data['my-suggestion'][0]['options']
    assert len(results) == 1
    assert results[0]['text'] == 'trying out Elasticsearch'


@asyncio.coroutine
def test_percolate(client, index):
    mapping = {
        "testdoc": {
            "properties": {
                "message": {
                    "type": "string"
                }
            }
        }
    }
    yield from client.indices.create(index)
    yield from client.indices.put_mapping(
        index,
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
    yield from client.index(index, '.percolator',
                            percolator, '1',
                            refresh=True)

    b = {
        "doc": {
            "message": "A new bonsai tree in the office"
        }
    }
    # percolate a doc from b
    data = yield from client.percolate(
        index,
        'testdoc',
        body=b,
    )
    assert data['total'] == 1
    assert data['matches'][0] == {'_index': 'test_elasticsearch', '_id': '1'}

    # percolate_count gives only count, no matches
    data = yield from client.count_percolate(
        index,
        'testdoc',
        body=b,
    )

    assert data['total'] == 1
    assert 'matches' not in data


@asyncio.coroutine
def test_mpercolate(client, index):
    mapping = {
        "testdoc": {
            "properties": {
                "message": {
                    "type": "string"
                }
            }
        }
    }
    yield from client.indices.create(index)
    yield from client.indices.put_mapping(
        index,
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
    yield from client.index(index, '.percolator',
                            percolator, '1',
                            refresh=True)

    body = [
        {
            'percolate': {
                'index': index,
                'type': 'testdoc',
            }
        },
        {
            "doc": {
                "message": "A new bonsai tree in the office"
            }
        }
    ]

    data = yield from client.mpercolate(
        body,
        index,
        'testdoc',
    )

    assert len(data['responses']) == 1
    item = data['responses'][0]
    assert item['total'] == 1
    assert item['matches'][0] == {'_index': 'test_elasticsearch', '_id': '1'}


@asyncio.coroutine
def test_termvector(client, index):
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
    yield from client.indices.create(index)
    yield from client.indices.put_mapping(
        index,
        'testdoc',
        mapping,
    )

    doc = {
        'message': 'Hello world',
    }

    yield from client.index(index, 'testdoc',
                            doc, '1',
                            refresh=True)

    data = yield from client.termvector(index, 'testdoc', '1')

    vector_data = data['term_vectors']['message']
    assert vector_data['field_statistics'] == {
        "sum_doc_freq": 2,
        "doc_count": 1,
        "sum_ttf": 2
    }
    assert 'hello' in vector_data['terms']
    assert 'world' in vector_data['terms']


@asyncio.coroutine
def test_mtermvectors(client, index):
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
    yield from client.indices.create(index)
    yield from client.indices.put_mapping(
        index,
        'testdoc',
        mapping,
    )

    doc = {
        'message': 'Hello world',
    }

    yield from client.index(index, 'testdoc',
                            doc, '1',
                            refresh=True)
    doc = {
        'message': 'Second term',
    }

    yield from client.index(index, 'testdoc',
                            doc, '2',
                            refresh=True)

    data = yield from client.mtermvectors(
        index, 'testdoc', ids='1,2'
    )

    assert len(data['docs']) == 2
    assert 'term_vectors' in data['docs'][0]
    assert 'term_vectors' in data['docs'][1]


@asyncio.coroutine
def test_scripts_management(client, index):
    script = {'script': 'log(_score * 2)'}

    # adding
    yield from client.put_script('groovy', 'test_script', script)

    # getting and checking
    got_script = yield from client.get_script('groovy', 'test_script')
    assert script['script'] == got_script['script']

    # deleting
    yield from client.delete_script('groovy', 'test_script')
    with pytest.raises(NotFoundError):
        got_script = yield from client.get_script(
            'groovy', 'test_script'
        )


@pytest.mark.xfail
@asyncio.coroutine
def test_scripts_execution(client, index):
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
                "lang": "painless",
                "script_id": "calculate-score",
                "params": {
                    "val": 2,
                }
            }
        }
    }

    yield from client.index(index, 'testdoc',
                            MESSAGES[0], '1',
                            refresh=True)

    yield from client.put_script('groovy', 'calculate-score', script)
    data = yield from client.search(index, 'testdoc', query)
    res = data['hits']['hits'][0]['fields']['test1'][0]
    assert res == 4  # 2*2


@asyncio.coroutine
def test_templates_management(client, index):
    template = {
        "template": {
            "query": {
                "match": {
                    "user": "{{query_string}}"
                }
            }
        }
    }

    yield from client.put_template('test_template', template)

    data = yield from client.get_template('test_template')
    assert data == {'lang': 'mustache',
                    '_version': 1,
                    '_id': 'test_template',
                    'found': True,
                    'template':
                        '{"query":{"match":{"user":"{{query_string}}"}}}'}

    yield from client.delete_template('test_template')
    with pytest.raises(NotFoundError):
        yield from client.get_template('test_template')


@asyncio.coroutine
def test_template_search(client, index):
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
        yield from client.index(
            index, 'testdoc', MESSAGES[0], '1',
            refresh=True
        )

        yield from client.put_template('test_template', template)

        data = yield from client.search_template(
            index, 'testdoc', body=search_body
        )
        assert data['hits']['total'] == 1


@asyncio.coroutine
def test_search_shards(client, index):
    yield from client.index(
        index, 'testdoc', MESSAGES[0], '1',
        refresh=True
    )
    data = yield from client.search_shards(
        index, 'testdoc'
    )
    assert 'nodes' in data
    assert len(data['nodes']) > 0
    assert 'shards' in data
    assert len(data['shards']) > 0
