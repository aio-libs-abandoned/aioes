import asyncio
import pytest
from aioes.exception import NotFoundError, RequestError

MESSAGE = {
    "user": "Johny Mnemonic",
    "birthDate": "2109-11-15T14:12:12",
    "message": "trying out Elasticsearch",
    "skills": ["Python", "PHP", "HTML", "C++", ".NET", "JavaScript"],
    "counter": 0,
    "test_field": "this, is a test 125 !"}


INDEX = 'test_elasticsearch'


@asyncio.coroutine
def test_analyze(client, es_tag):
    if es_tag > (5, 0):
        kwargs = dict(filter='lowercase')
    else:
        kwargs = dict(filters='lowercase')

    data = yield from client.indices.analyze(
        text='this, is a test 125 !',
        analyzer='standard',
        **kwargs)
    assert len(data['tokens']) == 5
    assert data['tokens'][0]['token'] == 'this'
    assert data['tokens'][1]['token'] == 'is'
    assert data['tokens'][2]['token'] == 'a'
    assert data['tokens'][3]['token'] == 'test'
    assert data['tokens'][4]['token'] == '125'
    assert data['tokens'][4]['type'] == '<NUM>'


@pytest.mark.es_tag(max=(2, 4), reason="params mess")
@asyncio.coroutine
def test_analyze_more(client, es_tag):

    data = yield from client.indices.analyze(
        text='THIS IS A <b>test</b>',
        tokenizer='keyword',
        token_filters='lowercase',
        char_filters='html_strip')
    assert data['tokens'][0]['token'] == 'this is a test'

    with pytest.raises(RequestError):
        yield from client.indices.analyze(
            analyzer='standard',
            filters='lowercase',
            field='w')


@asyncio.coroutine
def test_create(client):
    data = yield from client.indices.create(
        INDEX, timeout='1s', master_timeout='1s')
    assert data['acknowledged']


@pytest.mark.parametrize('kwargs', [
    dict(timeout=1),
    dict(timeout='1'),
    dict(timeout='1.1'),
    dict(master_timeout=1),
    dict(master_timeout='1'),
    dict(master_timeout='1.1'),
    ], ids=str)
@asyncio.coroutine
def test_create_errors(client, kwargs):
    with pytest.raises(RequestError):
        assert (yield from client.indices.create(INDEX, **kwargs)) is None


@asyncio.coroutine
def test_refresh(client):
    yield from client.index(INDEX, 'type', MESSAGE, '1')
    data = yield from client.indices.refresh(INDEX)
    assert '_shards' in data
    yield from client.indices.refresh(
        INDEX,
        allow_no_indices=False, expand_wildcards='closed',
        ignore_unavailable=True, ignore_indices='', force=True)
    with pytest.raises(TypeError):
        yield from client.indices.refresh(
            INDEX, expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.refresh(
            INDEX, expand_wildcards='1')


@asyncio.coroutine
def test_flush(client):
    yield from client.index(INDEX, 'type', MESSAGE, '1')
    data = yield from client.indices.flush(INDEX)
    assert '_shards' in data
    yield from client.indices.flush(
        INDEX, full=True,
        allow_no_indices=False, expand_wildcards='closed',
        ignore_unavailable=True, ignore_indices='', force=True)
    with pytest.raises(TypeError):
        yield from client.indices.flush(
            INDEX, expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.flush(
            INDEX, expand_wildcards='1')


@asyncio.coroutine
def test_open(client):
    yield from client.indices.create(INDEX)
    data = yield from client.indices.open(
        INDEX, timeout='10m', master_timeout='10m',
        allow_no_indices=False, expand_wildcards='closed',
        ignore_unavailable=True)
    assert data['acknowledged']
    data = yield from client.indices.open(INDEX)
    with pytest.raises(TypeError):
        yield from client.indices.open(INDEX,
                                       expand_wildcards=1,
                                       ignore_unavailable=True)
    with pytest.raises(ValueError):
        yield from client.indices.open(INDEX,
                                       expand_wildcards='1')


@asyncio.coroutine
def test_close(client):
    yield from client.index(INDEX, 'type',
                            MESSAGE,
                            '1')
    yield from client.cluster.health(
        INDEX,
        wait_for_status='yellow')
    data = yield from client.indices.close(INDEX)
    assert data['acknowledged']

    data = yield from client.indices.close(
        INDEX,
        timeout='1s', master_timeout='1s',
        expand_wildcards='open',
        allow_no_indices=True,
        ignore_unavailable=True)
    assert data['acknowledged']
    with pytest.raises(TypeError):
        yield from client.indices.close(
            INDEX,
            expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.close(
            INDEX,
            expand_wildcards='1')


@asyncio.coroutine
def test_delete(client):
    yield from client.index(INDEX, 'type', MESSAGE, '1')
    data = yield from client.indices.delete(INDEX)
    assert data['acknowledged']
    with pytest.raises(NotFoundError):
        yield from client.indices.delete(
            INDEX, timeout='1s', master_timeout='1s')
    assert data['acknowledged']


@asyncio.coroutine
def test_exists(client):
    yield from client.index(INDEX, 'type', MESSAGE, '1')
    data = yield from client.indices.exists(
        INDEX,
        allow_no_indices=False,
        expand_wildcards='closed',
        ignore_unavailable=False,
        local=False)
    assert data
    data = yield from client.indices.exists(INDEX+'123')
    assert not data
    with pytest.raises(TypeError):
        yield from client.indices.exists(
            INDEX, expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.exists(
            INDEX, expand_wildcards='1')


@asyncio.coroutine
def test_exists_type(client):
    yield from client.index(INDEX, 'type', MESSAGE, '1')
    yield from client.indices.refresh(INDEX)
    data = yield from client.indices.exists_type(
        INDEX, 'type', allow_no_indices=False)
    assert data
    data = yield from client.indices.exists_type(
        INDEX, 'ert', expand_wildcards='open')
    assert not data
    with pytest.raises(TypeError):
        yield from client.indices.exists_type(
            INDEX, '', expand_wildcards=1,
            allow_no_indices=True,
            ignore_unavailable=True,
            ignore_indices=True,
            local=True)
    with pytest.raises(ValueError):
        yield from client.indices.exists_type(
            INDEX, '', expand_wildcards='1')


@asyncio.coroutine
def test_get_settings(client):
    yield from client.index(INDEX, 'type', MESSAGE, '1')
    yield from client.indices.refresh(INDEX)
    data = yield from client.indices.get_settings()
    assert INDEX in data
    data = yield from client.indices.get_settings(
        expand_wildcards='open',
        ignore_indices='',
        flat_settings=False,
        ignore_unavailable=False,
        local=True)
    assert INDEX in data
    with pytest.raises(TypeError):
        yield from client.indices.get_settings(expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.indices.get_settings(expand_wildcards='1')


@asyncio.coroutine
def test_put_settings(client):
    yield from client.index(INDEX, 'type', MESSAGE, '1')
    yield from client.indices.refresh(INDEX)
    data = yield from client.indices.put_settings(
        {"index": {"number_of_replicas": 2}}, INDEX)
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


@pytest.mark.skip("indices status is deprecated since 1.2.0")
@asyncio.coroutine
def test_status(client):
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
def test_stats(client):
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
def test_segments(client):
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
def test_optimize(client):
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
def test_validate_query(client):
    yield from client.indices.create(INDEX)
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
def test_clear_cache(client):
    yield from client.indices.create(INDEX)
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
def test_recovery(client):
    yield from client.index(INDEX, 'type', MESSAGE, '1')
    data = yield from client.indices.refresh(INDEX)
    data = yield from client.indices.recovery()
    assert INDEX in data
    data = yield from client.indices.recovery(
        active_only=False,
        detailed=True,
        human=True)


@asyncio.coroutine
def test_mapping(client, es_tag):
    yield from client.indices.create(INDEX)
    DOCTYPE = 'testdoc'
    if es_tag < (5, 0):
        type_ = 'string'
    else:
        type_ = 'text'
    mapping = {
        DOCTYPE: {
            'properties': {
                'message': {
                    'type': type_,
                }
            }
        }
    }
    # PUT
    data = yield from client.indices.put_mapping(INDEX, DOCTYPE, mapping)
    assert data['acknowledged']

    # GET
    data = yield from client.indices.get_mapping(INDEX, DOCTYPE)
    assert data[INDEX]['mappings'] == mapping

    # DELETE
    # NOTE: it is not possible to delete mapping since 2.0
    if es_tag < (2, 0):
        yield from client.indices.delete_mapping(INDEX, DOCTYPE)
        data = yield from client.indices.get_mapping(INDEX, DOCTYPE)
        assert not data


@asyncio.coroutine
def test_get_field_mapping(client, es_tag):
    # create index
    yield from client.index(INDEX, 'type', MESSAGE, '1')
    rt = yield from client.indices.get_field_mapping(
        'message', index=INDEX
    )
    # dude, you are so deep
    if es_tag < (5, 0):
        data = {'message': {'type': 'string'}}
    else:
        data = {'message': {
            "type": "text", "fields": {
                "keyword": {"type": "keyword", "ignore_above": 256}
                }
            }}
    assert rt[INDEX]['mappings']['type']['message']['mapping'] == data


@pytest.mark.es_tag(max=(5, 0), reason='deprecated since es 2.3')
@asyncio.coroutine
def test_warmers(client):
    # create index
    yield from client.index(INDEX, 'type', MESSAGE, '1')

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
        index=INDEX, name='warmer', body=b
    )

    a = yield from client.indices.get_warmer(name='warmer')
    assert 'warmer' in a[INDEX]['warmers'].keys()

    yield from client.indices.delete_warmer(
        name='warmer', index=INDEX
    )
    a = yield from client.indices.get_warmer(name='warmer')
    assert not a


@asyncio.coroutine
def test_alias(client):
    # create index
    yield from client.index(INDEX, 'type', MESSAGE, '1')

    al = yield from client.indices.exists_alias('alias')
    assert not al
    al = yield from client.indices.get_alias(INDEX, 'alias')
    assert al == {}
    yield from client.indices.put_alias('alias', INDEX)
    al = yield from client.indices.exists_alias('alias')
    assert al
    yield from client.indices.update_aliases(body={
        "actions": [
            {"remove": {"index": INDEX, "alias": "alias"}},
            {"add": {"index": INDEX, "alias": "alias2"}}
        ]
    })
    al = yield from client.indices.exists_alias('alias2')
    assert al


@pytest.mark.es_tag(max=(2, 4))
@asyncio.coroutine
def test_aliases(client):
    yield from client.index(INDEX, 'type', MESSAGE, '1')

    al = yield from client.indices.get_aliases(INDEX, 'alias')
    assert al == {INDEX: {'aliases': {}}}

    yield from client.indices.put_alias('alias', INDEX)
    al = yield from client.indices.exists_alias('alias')
    assert al
    yield from client.indices.update_aliases(body={
        "actions": [
            {"remove": {"index": INDEX, "alias": "alias"}},
            {"add": {"index": INDEX, "alias": "alias2"}}
        ]
    })
    al = yield from client.indices.exists_alias('alias2')
    assert al
    yield from client.indices.delete_alias(INDEX, 'alias2')
    al = yield from client.indices.get_aliases(INDEX, 'alias')
    assert al == {INDEX: {'aliases': {}}}


@asyncio.coroutine
def test_templates(client):
    b = {
        "template": INDEX,
        "settings": {
            "number_of_shards": '1'
        },
    }
    try:
        t = yield from client.indices.exists_template('template')
        assert not t
        yield from client.indices.put_template('template', b)
        t = yield from client.indices.exists_template('template')
        assert t
        t = yield from client.indices.get_template('template')
        assert 'template' in t
        assert 'settings' in t['template']
        assert 'index' in t['template']['settings']
        assert 'number_of_shards' in t['template']['settings']['index']
        assert t['template']['settings']['index']['number_of_shards'] == \
            b['settings']['number_of_shards']
    finally:
        yield from client.indices.delete_template('template')
        t = yield from client.indices.exists_template('template')
        assert not t
