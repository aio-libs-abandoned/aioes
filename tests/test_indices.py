import asyncio
import pytest
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
def test_analize(client):
    data = yield from client.indices.analyze(
        text='this, is a test 125 !',
        analyzer='standard',
        filters='lowercase')
    assert len(data['tokens']) == 5
    assert data['tokens'][0]['token'] == 'this'
    assert data['tokens'][1]['token'] == 'is'
    assert data['tokens'][2]['token'] == 'a'
    assert data['tokens'][3]['token'] == 'test'
    assert data['tokens'][4]['token'] == '125'
    assert data['tokens'][4]['type'] == '<NUM>'

    data = yield from client.indices.analyze(
        text='this is a <b>test</b>',
        tokenizer='keyword',
        token_filters='lowercase',
        char_filters='html_strip',
        prefer_local=True)
    assert data['tokens'][0]['token'] == 'this is a test'

    with pytest.raises(RequestError):
        yield from client.indices.analyze(
            analyzer='standard',
            filters='lowercase',
            field='w')


@asyncio.coroutine
def test_create(client, index):
    data = yield from client.indices.create(
        index, timeout=1000, master_timeout=1000)
    assert data['acknowledged']


@asyncio.coroutine
def test_refresh(client, index):
    yield from client.index(index, 'type', MESSAGE, '1')
    data = yield from client.indices.refresh(index)
    assert '_shards' in data
    yield from client.indices.refresh(
        index,
        allow_no_indices=False, expand_wildcards='closed',
        ignore_unavailable=True, ignore_indices='', force=True)
    with pytest.raises(TypeError):
        yield from client.indices.refresh(
            index, expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.refresh(
            index, expand_wildcards='1')


@asyncio.coroutine
def test_flush(client, index):
    yield from client.index(index, 'type', MESSAGE, '1')
    data = yield from client.indices.flush(index)
    assert '_shards' in data
    yield from client.indices.flush(
        index, full=True,
        allow_no_indices=False, expand_wildcards='closed',
        ignore_unavailable=True, ignore_indices='', force=True)
    with pytest.raises(TypeError):
        yield from client.indices.flush(
            index, expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.flush(
            index, expand_wildcards='1')


@asyncio.coroutine
def test_open(client, index):
    yield from client.indices.create(index)
    data = yield from client.indices.open(
        index, timeout='10m', master_timeout='10m',
        allow_no_indices=False, expand_wildcards='closed',
        ignore_unavailable=True)
    assert data['acknowledged']
    data = yield from client.indices.open(index)
    with pytest.raises(TypeError):
        yield from client.indices.open(index,
                                       expand_wildcards=1,
                                       ignore_unavailable=True)
    with pytest.raises(ValueError):
        yield from client.indices.open(index,
                                       expand_wildcards='1')


@asyncio.coroutine
def test_close(client, index):
    yield from client.index(index, 'type',
                            MESSAGE,
                            '1')
    yield from client.cluster.health(
        index,
        wait_for_status='yellow')
    data = yield from client.indices.close(index)
    assert data['acknowledged']

    data = yield from client.indices.close(
        index,
        timeout='1s', master_timeout='1s',
        expand_wildcards='open',
        allow_no_indices=True,
        ignore_unavailable=True)
    assert data['acknowledged']
    with pytest.raises(TypeError):
        yield from client.indices.close(
            index,
            expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.close(
            index,
            expand_wildcards='1')


@asyncio.coroutine
def test_delete(client, index):
    yield from client.index(index, 'type', MESSAGE, '1')
    data = yield from client.indices.delete(index)
    assert data['acknowledged']
    with pytest.raises(NotFoundError):
        yield from client.indices.delete(
            index, timeout='1s', master_timeout='1s')
    assert data['acknowledged']


@asyncio.coroutine
def test_exists(client, index):
    yield from client.index(index, 'type', MESSAGE, '1')
    data = yield from client.indices.exists(
        index,
        allow_no_indices=False,
        expand_wildcards='closed',
        ignore_unavailable=False,
        local=False)
    assert data
    data = yield from client.indices.exists(index+'123')
    assert not data
    with pytest.raises(TypeError):
        yield from client.indices.exists(
            index, expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.exists(
            index, expand_wildcards='1')


@asyncio.coroutine
def test_exists_type(client, index):
    yield from client.index(index, 'type', MESSAGE, '1')
    yield from client.indices.refresh(index)
    data = yield from client.indices.exists_type(
        index, 'type', allow_no_indices=False)
    assert data
    data = yield from client.indices.exists_type(
        index, 'ert', expand_wildcards='open')
    assert not data
    with pytest.raises(TypeError):
        yield from client.indices.exists_type(
            index, '', expand_wildcards=1,
            allow_no_indices=True,
            ignore_unavailable=True,
            ignore_indices=True,
            local=True)
    with pytest.raises(ValueError):
        yield from client.indices.exists_type(
            index, '', expand_wildcards='1')


@asyncio.coroutine
def test_get_settings(client, index):
    yield from client.index(index, 'type', MESSAGE, '1')
    yield from client.indices.refresh(index)
    data = yield from client.indices.get_settings()
    assert index in data
    data = yield from client.indices.get_settings(
        expand_wildcards='open',
        ignore_indices='',
        flat_settings=False,
        ignore_unavailable=False,
        local=True)
    assert index in data
    with pytest.raises(TypeError):
        yield from client.indices.get_settings(expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.get_settings(expand_wildcards='1')


@asyncio.coroutine
def test_put_settings(client, index):
    yield from client.index(index, 'type', MESSAGE, '1')
    yield from client.indices.refresh(index)
    data = yield from client.indices.put_settings(
        {"index": {"number_of_replicas": 2}}, index)
    assert data['acknowledged']
    with pytest.raises(RequestError):
        yield from client.indices.put_settings(
            {"index": {"number_of_replicas": 2}},
            allow_no_indices=True,
            expand_wildcards='open',
            flat_settings=False,
            ignore_unavailable=False,
            master_timeout='1s')
    assert data['acknowledged']
    with pytest.raises(TypeError):
        yield from client.indices.put_settings(
            {}, expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.put_settings(
            {}, expand_wildcards='1')


@asyncio.coroutine
def test_status(client, index):
    data = yield from client.indices.status()
    assert 'indices' in data
    data = yield from client.indices.status(
        ignore_indices='',
        allow_no_indices=True,
        recovery=False,
        snapshot=False,
        operation_threading='',
        expand_wildcards='open',
        ignore_unavailable=False,
        human=True)
    assert '_shards' in data
    with pytest.raises(TypeError):
        yield from client.indices.status(expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.status(expand_wildcards='1')


@asyncio.coroutine
def test_stats(client, index):
    data = yield from client.indices.stats()
    assert 'indices' in data
    data = yield from client.indices.stats(
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
    assert '_all' in data
    with pytest.raises(TypeError):
        yield from client.indices.stats(expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.stats(expand_wildcards='1')
    with pytest.raises(TypeError):
        yield from client.indices.stats(level=1)
    with pytest.raises(ValueError):
        yield from client.indices.stats(level='1')
    with pytest.raises(TypeError):
        yield from client.indices.stats(metric=1)
    with pytest.raises(ValueError):
        yield from client.indices.stats(metric='1')


@asyncio.coroutine
def test_segments(client, index):
    data = yield from client.indices.segments()
    assert 'indices' in data
    assert '_shards' in data
    data = yield from client.indices.segments(
        allow_no_indices=True,
        ignore_indices=True,
        ignore_unavailable=True,
        expand_wildcards='open',
        human=True)
    assert 'indices' in data
    assert '_shards' in data
    with pytest.raises(TypeError):
        yield from client.indices.segments(expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.segments(expand_wildcards='1')


@asyncio.coroutine
def test_optimize(client, index):
    data = yield from client.indices.optimize()
    assert '_shards' in data
    data = yield from client.indices.optimize(
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
    assert '_shards' in data
    with pytest.raises(TypeError):
        yield from client.indices.optimize(expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.optimize(expand_wildcards='1')


@asyncio.coroutine
def test_validate_query(client, index):
    data = yield from client.indices.validate_query()
    assert '_shards' in data
    yield from client.indices.validate_query(
        explain=True,
        allow_no_indices=True,
        q='',
        ignore_indices=True,
        source='',
        operation_threading='',
        expand_wildcards='open',
        ignore_unavailable=False)
    with pytest.raises(TypeError):
        yield from client.indices.validate_query(expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.validate_query(expand_wildcards='1')


@asyncio.coroutine
def test_clear_cache(client, index):
    data = yield from client.indices.clear_cache()
    assert '_shards' in data
    yield from client.indices.clear_cache(
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
    assert '_shards' in data
    with pytest.raises(TypeError):
        yield from client.indices.clear_cache(expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.clear_cache(expand_wildcards='1')


@asyncio.coroutine
def test_recovery(client, index):
    yield from client.index(index, 'type', MESSAGE, '1')
    data = yield from client.indices.refresh(index)
    data = yield from client.indices.recovery()
    assert index in data
    data = yield from client.indices.recovery(
        active_only=False,
        detailed=True,
        human=True)


@asyncio.coroutine
def test_mapping(client, index):
    yield from client.indices.create(index)
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
    data = yield from client.indices.put_mapping(
        index,
        'testdoc',
        mapping,
    )
    assert data['acknowledged']

    # GET
    data = yield from client.indices.get_mapping(
        index,
        'testdoc',
    )
    assert data['elastic_search']['mappings'] == mapping

    # DELETE
    yield from client.indices.delete_mapping(
        index,
        'testdoc',
    )
    data = yield from client.indices.get_mapping(
        index,
        'testdoc',
    )
    assert not data


@asyncio.coroutine
def test_get_field_mapping(client, index):
    # create index
    yield from client.index(index, 'type', MESSAGE, '1')
    rt = yield from client.indices.get_field_mapping(
        'message', index=index
    )
    # dude, you are so deep
    assert rt[index]['mappings']['type']['message']['mapping'] == \
        {'message': {'type': 'string'}}


@asyncio.coroutine
def test_warmers(client, index):
    # create index
    yield from client.index(index, 'type', MESSAGE, '1')

    a = yield from client.indices.get_warmer(name='warmer')
    assert not a

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
    yield from client.indices.put_warmer(
        index=index, name='warmer', body=b
    )

    a = yield from client.indices.get_warmer(name='warmer')
    assert 'warmer' in a[index]['warmers'].keys()

    yield from client.indices.delete_warmer(
        name='warmer', index=index
    )
    a = yield from client.indices.get_warmer(name='warmer')
    assert not a


@asyncio.coroutine
def test_aliases(client, index):
    # create index
    yield from client.index(index, 'type', MESSAGE, '1')

    al = yield from client.indices.exists_alias('alias')
    assert not al
    al = yield from client.indices.get_alias('alias')
    assert {} == al
    al = yield from client.indices.get_aliases('alias')
    assert {} == al

    yield from client.indices.put_alias('alias', index)
    al = yield from client.indices.exists_alias('alias')
    assert al
    yield from client.indices.update_aliases(body={
        "actions": [
            {"remove": {"index": index, "alias": "alias"}},
            {"add": {"index": index, "alias": "alias2"}}
        ]
    })
    al = yield from client.indices.exists_alias('alias2')
    assert al
    yield from client.indices.delete_alias(index, 'alias2')
    al = yield from client.indices.get_aliases('alias')
    assert not al


@asyncio.coroutine
def test_templates(client, index):
    b = {
        "template": index,
        "settings": {
            "number_of_shards": '1'
        },
    }
    t = yield from client.indices.exists_template('template')
    assert not t
    yield from client.indices.put_template('template', b)
    t = yield from client.indices.exists_template('template')
    assert t
    t = yield from client.indices.get_template('template')
    assert t['template']['settings']['index.number_of_shards'] == \
        b['settings']['number_of_shards']
    yield from client.indices.delete_template('template')
    t = yield from client.indices.exists_template('template')
    assert not t
