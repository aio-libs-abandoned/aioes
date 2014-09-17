import asyncio
import json
from .cat import CatClient
from .cluster import ClusterClient
from .indices import IndicesClient
from .nodes import NodesClient
from .snapshot import SnapshotClient
from aioes.transport import Transport
from .utils import _make_path
from aioes.exception import (NotFoundError, TransportError)


default = object()


class Elasticsearch:
    def __init__(self, endpoints, *, loop=None, **kwargs):
        self._transport = Transport(endpoints, loop=loop, **kwargs)
        self._cat = CatClient(self)
        self._cluster = ClusterClient(self)
        self._indices = IndicesClient(self)
        self._nodes = NodesClient(self)
        self._snapshot = SnapshotClient(self)

    @property
    def indices(self):
        return self._indices

    @property
    def cluster(self):
        return self._cluster

    @property
    def cat(self):
        return self._cat

    @property
    def nodes(self):
        return self._nodes

    @property
    def snapshot(self):
        return self._snapshot

    @property
    def transport(self):
        return self._transport

    def __repr__(self):
        return "<Elasticsearch [{}]".format(self.transport)

    def _bulk_body(self, body):
        return '\n'.join(map(json.dumps, body)) + '\n'

    def close(self):
        self.transport.close()

    @asyncio.coroutine
    def ping(self):
        """
        Returns True if the cluster is up, False otherwise.
        """
        try:
            yield from self.transport.perform_request('HEAD', '/')
        except TransportError:
            return False
        return True

    @asyncio.coroutine
    def info(self):
        """
        Get the basic info from the current cluster.
        """
        _, data = yield from self.transport.perform_request('GET', '/')
        return data

# index API
    @asyncio.coroutine
    def create(self, index, doc_type, body, id=None, *,
               consistency=default, parent=default, percolate=default,
               refresh=default, replication=default, routing=default,
               timeout=default, timestamp=default, ttl=default,
               version=default, version_type=default):
        """
        Adds a typed JSON document in a specific index, making it searchable.
        Behind the scenes this method calls index(..., op_type='create')
        """
        data = yield from self.index(
            index, doc_type, body, id,
            consistency=consistency, parent=parent, percolate=percolate,
            refresh=refresh, replication=replication, routing=routing,
            timeout=timeout, timestamp=timestamp, ttl=ttl,
            version=version, version_type=version_type, op_type='create')
        return data

    @asyncio.coroutine
    def index(self, index, doc_type, body, id=None, *,
              consistency=default, op_type=default, parent=default,
              percolate=default, refresh=default, replication=default,
              routing=default, timeout=default, timestamp=default,
              ttl=default, version=default, version_type=default):
        """
        Adds or updates a typed JSON document in a specific index, making it
        searchable.
        """
        params = {}
        if consistency is not default:
            if not isinstance(consistency, str):
                raise TypeError("'consistency' parameter is not a string")
            elif consistency.lower() in ('one', 'quorum', 'all'):
                params['consistency'] = consistency.lower()
            else:
                raise ValueError("'consistency' parameter should be one of"
                                 " 'one', 'quorum', 'all'")

        if op_type is not default:
            if not isinstance(op_type, str):
                raise TypeError("'op_type' parameter is not a string")
            elif op_type.lower() in ('index', 'create'):
                params['op_type'] = op_type.lower()
            else:
                raise ValueError(
                    "'op_type' parameter should be one of 'index', 'create'")

        if parent is not default:
            params['parent'] = parent
        if percolate is not default:
            params['percolate'] = percolate
        if refresh is not default:
            params['refresh'] = bool(refresh)
        if replication is not default:
            if not isinstance(replication, str):
                raise TypeError("'replication' parameter is not a string")
            elif replication.lower() in ('async', 'sync'):
                params['replication'] = replication.lower()
            else:
                raise ValueError(
                    "'replication' parameter should be one of 'async', 'sync'")
        if routing is not default:
            params['routing'] = routing
        if timeout is not default:
            params['timeout'] = timeout
        if timestamp is not default:
            params['timestamp'] = timestamp
        if ttl is not default:
            params['ttl'] = ttl
        if version is not default:
            params['version'] = int(version)

        if version_type is not default:
            if not isinstance(version_type, str):
                raise TypeError("'version_type' parameter is not a string")
            elif version_type.lower() in ('internal', 'external',
                                          'external_gt', 'external_gte',
                                          'force'):
                params['version_type'] = version_type.lower()
            else:
                raise ValueError("'version_type' parameter should be one of "
                                 "'internal', 'external', 'external_gt', "
                                 "'external_gte', 'force'")

        _, data = yield from self.transport.perform_request(
            'PUT' if id else 'POST',
            _make_path(index, doc_type, id),
            params=params,
            body=body)

        return data

# get API
    @asyncio.coroutine
    def exists(self, index, id, doc_type='_all', *, parent=default,
               preference=default, realtime=default, refresh=default,
               routing=default):
        """
        Returns a boolean indicating whether or not given document exists
        in Elasticsearch.
        """
        params = {}
        if parent is not default:
            params['parent'] = parent
        if preference is not default:
            params['preference'] = preference
        if realtime is not default:
            params['realtime'] = bool(realtime)
        if refresh is not default:
            params['refresh'] = bool(refresh)
        if routing is not default:
            params['routing'] = routing

        try:
            yield from self.transport.perform_request(
                'HEAD',
                _make_path(index, doc_type, id),
                params=params)
        except NotFoundError:
            return False
        return True

    @asyncio.coroutine
    def get(self, index, id, doc_type='_all', *,
            _source=default, _source_exclude=default,
            _source_include=default, fields=default,
            parent=default, preference=default, realtime=default,
            refresh=default, routing=default, version=default,
            version_type=default):
        """
        Get a typed JSON document from the index based on its id.
        """
        params = {}
        if _source is not default:
            params['_source'] = _source
        if _source_exclude is not default:
            params['_source_exclude'] = _source_exclude
        if _source_include is not default:
            params['_source_include'] = _source_include
        if fields is not default:
            params['fields'] = fields
        if parent is not default:
            params['parent'] = parent
        if preference is not default:
            params['preference'] = preference
        if realtime is not default:
            params['realtime'] = bool(realtime)
        if refresh is not default:
            params['refresh'] = bool(refresh)
        if routing is not default:
            params['routing'] = routing
        if version is not default:
            params['version'] = int(version)

        if version_type is not default:
            if not isinstance(version_type, str):
                raise TypeError("'version_type' parameter is not a string")
            elif version_type.lower() in ('internal', 'external',
                                          'external_gt', 'external_gte',
                                          'force'):
                params['version_type'] = version_type.lower()
            else:
                raise ValueError("'version_type' parameter should be one of "
                                 "'internal', 'external', 'external_gt', "
                                 "'external_gte', 'force'")

        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path(index, doc_type, id),
            params=params)

        return data

    @asyncio.coroutine
    def get_source(self, index, id, doc_type='_all', *,
                   _source=default, _source_exclude=default,
                   _source_include=default, parent=default,
                   preference=default, realtime=default, refresh=default,
                   routing=default, version=default,
                   version_type=default):
        """
        Get the source of a document by it's index, type and id.
        """
        params = {}
        if _source is not default:
            params['_source'] = _source
        if _source_exclude is not default:
            params['_source_exclude'] = _source_exclude
        if _source_include is not default:
            params['_source_include'] = _source_include
        if parent is not default:
            params['parent'] = parent
        if preference is not default:
            params['preference'] = preference
        if realtime is not default:
            params['realtime'] = bool(realtime)
        if refresh is not default:
            params['refresh'] = bool(refresh)
        if routing is not default:
            params['routing'] = routing
        if version is not default:
            params['version'] = int(version)

        if version_type is not default:
            if not isinstance(version_type, str):
                raise TypeError("'version_type' parameter is not a string")
            elif version_type.lower() in ('internal', 'external',
                                          'external_gt', 'external_gte',
                                          'force'):
                params['version_type'] = version_type.lower()
            else:
                raise ValueError("'version_type' parameter should be one of "
                                 "'internal', 'external', 'external_gt', "
                                 "'external_gte', 'force'")

        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path(index, doc_type, id, '_source'),
            params=params)

        return data

    @asyncio.coroutine
    def update(self, index, doc_type, id, body=None, *,
               consistency=default, fields=default, lang=default,
               parent=default, refresh=default, replication=default,
               retry_on_conflict=default, routing=default, script=default,
               timeout=default, timestamp=default, ttl=default,
               version=default, version_type=default):
        """
        Update a document based on a script or partial data provided.
        """
        params = {}
        if consistency is not default:
            if not isinstance(consistency, str):
                raise TypeError("'consistency' parameter is not a string")
            elif consistency.lower() in ('one', 'quorum', 'all'):
                params['consistency'] = consistency.lower()
            else:
                raise ValueError("'consistency' parameter should be one of "
                                 "'one', 'quorum', 'all'")
        if fields is not default:
            params['fields'] = fields
        if lang is not default:
            params['lang'] = lang
        if parent is not default:
            params['parent'] = parent
        if refresh is not default:
            params['refresh'] = bool(refresh)
        if replication is not default:
            if not isinstance(replication, str):
                raise TypeError("'replication' parameter is not a string")
            elif replication.lower() in ('async', 'sync'):
                params['replication'] = replication.lower()
            else:
                raise ValueError(
                    "'replication' parameter should be one of 'async', 'sync'")
        if retry_on_conflict is not default:
            params['retry_on_conflict'] = retry_on_conflict
        if routing is not default:
            params['routing'] = routing
        if script is not default:
            params['script'] = script
        if timeout is not default:
            params['timeout'] = timeout
        if timestamp is not default:
            params['timestamp'] = timestamp
        if ttl is not default:
            params['ttl'] = ttl
        if version is not default:
            params['version'] = int(version)

        if version_type is not default:
            if not isinstance(version_type, str):
                raise TypeError("'version_type' parameter is not a string")
            elif version_type.lower() in ('internal', 'external',
                                          'external_gt', 'external_gte',
                                          'force'):
                params['version_type'] = version_type.lower()
            else:
                raise ValueError("'version_type' parameter should be one of "
                                 "'internal', 'external', 'external_gt', "
                                 "'external_gte', 'force'")

        _, data = yield from self.transport.perform_request(
            'POST',
            _make_path(index, doc_type, id, '_update'),
            params=params,
            body=body)
        return data

    @asyncio.coroutine
    def mget(self, body, index=None, doc_type=None, *,
             _source=default, _source_exclude=default,
             _source_include=default, fields=default, parent=default,
             preference=default, realtime=default, refresh=default,
             routing=default):
        """
        Get multiple documents based on an index, type (optional) and ids.
        """
        params = {}
        if _source is not default:
            params['_source'] = _source
        if _source_exclude is not default:
            params['_source_exclude'] = _source_exclude
        if _source_include is not default:
            params['_source_include'] = _source_include
        if fields is not default:
            params['fields'] = fields
        if parent is not default:
            params['parent'] = parent
        if preference is not default:
            params['preference'] = preference
        if realtime is not default:
            params['realtime'] = bool(realtime)
        if refresh is not default:
            params['refresh'] = bool(refresh)
        if routing is not default:
            params['routing'] = routing

        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path(index, doc_type, '_mget'),
            params=params,
            body=body)

        return data

    @asyncio.coroutine
    def search(self, index=None, doc_type=None, body=None, *,
               _source=default, _source_exclude=default,
               _source_include=default, analyze_wildcard=default,
               analyzer=default, default_operator=default, df=default,
               explain=default, fields=default, indices_boost=default,
               lenient=default, allow_no_indices=default,
               expand_wildcards=default, ignore_unavailable=default,
               lowercase_expanded_terms=default, from_=default,
               preference=default, q=default, routing=default,
               scroll=default, search_type=default, size=default,
               sort=default, source=default, stats=default,
               suggest_field=default, suggest_mode=default,
               suggest_size=default, suggest_text=default,
               timeout=default, version=default):
        """
        Execute a search query and get back search hits that match the query.
        """
        if doc_type and index is None:
            index = '_all'

        params = {}
        if _source is not default:
            params['_source'] = _source
        if _source_exclude is not default:
            params['_source_exclude'] = _source_exclude
        if _source_include is not default:
            params['_source_include'] = _source_include
        if analyze_wildcard is not default:
            params['analyze_wildcard'] = bool(analyze_wildcard)
        if df is not default:
            params['df'] = df
        if explain is not default:
            params['explain'] = bool(explain)
        if fields is not default:
            params['fields'] = fields
        if indices_boost is not default:
            params['indices_boost'] = indices_boost
        if lenient is not default:
            params['lenient'] = bool(lenient)
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if lowercase_expanded_terms is not default:
            params['lowercase_expanded_terms'] = bool(lowercase_expanded_terms)
        # from is a reserved word so it cannot be used, use from_ instead
        if from_ is not default:
            params['from'] = int(from_)
        if preference is not default:
            params['preference'] = preference
        if q is not default:
            params['q'] = q
        if routing is not default:
            params['routing'] = routing
        if scroll is not default:
            params['scroll'] = scroll
        if size is not default:
            params['size'] = int(size)
        if sort is not default:
            params['sort'] = sort
        if source is not default:
            params['source'] = source
        if stats is not default:
            params['stats'] = stats
        if suggest_field is not default:
            params['suggest_field'] = suggest_field
        if suggest_size is not default:
            params['suggest_size'] = int(suggest_size)
        if suggest_text is not default:
            params['suggest_text'] = suggest_text
        if timeout is not default:
            params['timeout'] = timeout
        if version is not default:
            params['version'] = int(version)
        if analyzer is not default:
            params['analyzer'] = analyzer

        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be one"
                                 " of 'open', 'closed'")

        if suggest_mode is not default:
            if not isinstance(suggest_mode, str):
                raise TypeError("'suggest_mode' parameter is not a string")
            elif suggest_mode.lower() in ('missing', 'popular', 'always'):
                params['suggest_mode'] = suggest_mode.lower()
            else:
                raise ValueError("'suggest_mode' parameter should be one of "
                                 "'missing', 'popular', 'always'")

        if search_type is not default:
            if not isinstance(search_type, str):
                raise TypeError("'search_type' parameter is not a string")
            elif search_type.lower() in ('query_then_fetch',
                                         'query_and_fetch',
                                         'dfs_query_then_fetch',
                                         'dfs_query_and_fetch',
                                         'count',
                                         'scan'):
                params['search_type'] = search_type.lower()
            else:
                raise ValueError("'search_type' parameter should be one of "
                                 "'query_then_fetch', 'query_and_fetch', "
                                 "'dfs_query_then_fetch', "
                                 "'dfs_query_and_fetch', 'count', 'scan'")

        if default_operator is not default:
            if not isinstance(default_operator, str):
                raise TypeError("'default_operator' parameter is not a string")
            elif default_operator.upper() in ('AND', 'OR'):
                params['default_operator'] = default_operator.upper()
            else:
                raise ValueError("'default_operator' parameter should "
                                 "be one of 'AND', 'OR'")

        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path(index, doc_type, '_search'),
            params=params,
            body=body)

        return data

    @asyncio.coroutine
    def search_shards(self, index=None, doc_type=None, *,
                      allow_no_indices=default, expand_wildcards=default,
                      ignore_unavailable=default, local=default,
                      preference=default, routing=default):
        """
        The search shards api returns the indices and shards that a search
        request would be executed against. This can give useful feedback
        for working out issues or planning optimizations with routing and
        shard preferences.
       """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not "
                                "a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be"
                                 " one of 'open', 'closed'")
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if local is not default:
            params['local'] = local
        if preference is not default:
            params['preference'] = preference
        if routing is not default:
            params['routing'] = routing

        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path(index, doc_type, '_search_shards'),
            params=params)

        return data

    @asyncio.coroutine
    def search_template(self, index=None, doc_type=None, body=None, *,
                        allow_no_indices=default,
                        expand_wildcards=default,
                        ignore_unavailable=default, preference=default,
                        routing=default, scroll=default,
                        search_type=default):
        """
        A query that accepts a query template and a map of key/value pairs to
        fill in template parameters.
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not "
                                "a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be"
                                 " one of 'open', 'closed'")
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if preference is not default:
            params['preference'] = preference
        if routing is not default:
            params['routing'] = routing
        if scroll is not default:
            params['scroll'] = scroll
        if search_type is not default:
            if not isinstance(search_type, str):
                raise TypeError("'search_type' parameter is not a string")
            elif search_type.lower() in ('query_then_fetch',
                                         'query_and_fetch',
                                         'dfs_query_then_fetch',
                                         'dfs_query_and_fetch',
                                         'count',
                                         'scan'):
                params['search_type'] = search_type.lower()
            else:
                raise ValueError("'search_type' parameter should be one of "
                                 "'query_then_fetch', 'query_and_fetch', "
                                 "'dfs_query_then_fetch', "
                                 "'dfs_query_and_fetch', 'count', 'scan'")

        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path(index, doc_type, '_search', 'template'),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def explain(self, index, doc_type, id, body=None, *,
                _source=default, _source_exclude=default,
                _source_include=default, analyze_wildcard=default,
                analyzer=default, default_operator=default,
                df=default, fields=default, lenient=default,
                lowercase_expanded_terms=default, parent=default,
                preference=default, q=default, routing=default,
                source=default):
        """
        The explain api computes a score explanation for a query and a
        specific document. This can give useful feedback whether a document
        matches or didn't match a specific query.
        """
        params = {}
        if _source is not default:
            params['_source'] = _source
        if _source_exclude is not default:
            params['_source_exclude'] = _source_exclude
        if _source_include is not default:
            params['_source_include'] = _source_include
        if analyze_wildcard is not default:
            params['analyze_wildcard'] = bool(analyze_wildcard)
        if analyzer is not default:
            params['analyzer'] = analyzer
        if df is not default:
            params['df'] = df
        if fields is not default:
            params['fields'] = fields
        if lenient is not default:
            params['lenient'] = bool(lenient)
        if lowercase_expanded_terms is not default:
            params['lowercase_expanded_terms'] = bool(lowercase_expanded_terms)
        if parent is not default:
            params['parent'] = parent
        if preference is not default:
            params['preference'] = preference
        if q is not default:
            params['q'] = q
        if routing is not default:
            params['routing'] = routing
        if source is not default:
            params['source'] = source
        if default_operator is not default:
            if not isinstance(default_operator, str):
                raise TypeError("'default_operator' parameter is not a string")
            elif default_operator.upper() in ('AND', 'OR'):
                params['default_operator'] = default_operator.upper()
            else:
                raise ValueError("'default_operator' parameter should "
                                 "be one of 'AND', 'OR'")

        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path(index, doc_type, id, '_explain'),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def scroll(self, scroll_id, *, scroll=default):
        """
        Scroll a search request created by specifying the scroll parameter.
        """
        params = {}
        if scroll is not default:
            params['scroll'] = scroll

        _, data = yield from self.transport.perform_request(
            'GET',
            '/_search/scroll',
            params=params, body=scroll_id)

        return data

    @asyncio.coroutine
    def clear_scroll(self, scroll_id=None, body=None):
        """
        Clear the scroll request created by specifying the scroll parameter
        to search.
        """
        _, data = yield from self.transport.perform_request(
            'DELETE',
            _make_path('_search', 'scroll', scroll_id),
            body=body)

        return data

    @asyncio.coroutine
    def delete(self, index, doc_type=None, id=None, *,
               consistency=default, parent=default, refresh=default,
               replication=default, routing=default, timeout=default,
               version=default, version_type=default):
        """
        Delete a typed JSON document from a specific index based on its id.
        """
        params = {}
        if consistency is not default:
            if not isinstance(consistency, str):
                raise TypeError("'consistency' parameter is not a string")
            elif consistency.lower() in ('one', 'quorum', 'all'):
                params['consistency'] = consistency.lower()
            else:
                raise ValueError(
                    "'consistency' parameter should be one of "
                    "'one', 'quorum', 'all'")
        if replication is not default:
            if not isinstance(replication, str):
                raise TypeError("'replication' parameter is not a string")
            elif replication.lower() in ('async', 'sync'):
                params['replication'] = replication.lower()
            else:
                raise ValueError("'replication' parameter should be one of "
                                 "'async', 'sync'")
        if timeout is not default:
            params['timeout'] = timeout
        if parent is not default:
            params['parent'] = parent
        if refresh is not default:
            params['refresh'] = bool(refresh)
        if routing is not default:
            params['routing'] = routing
        if version is not default:
            params['version'] = int(version)

        if version_type is not default:
            if not isinstance(version_type, str):
                raise TypeError("'version_type' parameter is not a string")
            elif version_type.lower() in ('internal', 'external',
                                          'external_gt', 'external_gte',
                                          'force'):
                params['version_type'] = version_type.lower()
            else:
                raise ValueError("'version_type' parameter should be one of "
                                 "'internal', 'external', 'external_gt', "
                                 "'external_gte', 'force'")

        _, data = yield from self.transport.perform_request(
            'DELETE',
            _make_path(index, doc_type, id),
            params=params)

        return data

    @asyncio.coroutine
    def count(self, index=None, doc_type=None, body=None, *,
              allow_no_indices=default, expand_wildcards=default,
              ignore_unavailable=default, min_score=default,
              preference=default, q=default, routing=default,
              source=default):
        """
        Execute a query and get the number of matches for that query.
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if min_score is not default:
            params['min_score'] = int(min_score)
        if preference is not default:
            params['preference'] = preference
        if q is not default:
            params['q'] = q
        if routing is not default:
            params['routing'] = routing
        if source is not default:
            params['source'] = source

        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not "
                                "a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be"
                                 " one of 'open', 'closed'")

        _, data = yield from self.transport.perform_request(
            'POST',
            _make_path(index, doc_type, '_count'),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def bulk(self, body, index=None, doc_type=None, *,
             consistency=default, refresh=default, routing=default,
             replication=default, timeout=default):
        """
        Perform many index/delete operations in a single API call.
        """
        params = {}
        if consistency is not default:
            if not isinstance(consistency, str):
                raise TypeError("'consistency' parameter is not a string")
            elif consistency.lower() in ('one', 'quorum', 'all'):
                params['consistency'] = consistency.lower()
            else:
                raise ValueError("'consistency' parameter should be one of "
                                 "'one', 'quorum', 'all'")
        if refresh is not default:
            params['refresh'] = bool(refresh)
        if routing is not default:
            params['routing'] = routing
        if replication is not default:
            if not isinstance(replication, str):
                raise TypeError("'replication' parameter is not a string")
            elif replication.lower() in ('async', 'sync'):
                params['replication'] = replication.lower()
            else:
                raise ValueError("'replication' parameter should be one of"
                                 " 'async', 'sync'")
        if timeout is not default:
            params['timeout'] = timeout

        _, data = yield from self.transport.perform_request(
            'POST',
            _make_path(index, doc_type, '_bulk'),
            params=params,
            body=self._bulk_body(body))

        return data

    @asyncio.coroutine
    def msearch(self, body, index=None, doc_type=None, *,
                search_type=default):
        """
        Execute several search requests within the same API.
        """
        params = {}
        if search_type is not default:
            if not isinstance(search_type, str):
                raise TypeError("'search_type' parameter is not a string")
            elif search_type.lower() in ('query_then_fetch',
                                         'query_and_fetch',
                                         'dfs_query_then_fetch',
                                         'dfs_query_and_fetch',
                                         'count',
                                         'scan'):
                params['search_type'] = search_type.lower()
            else:
                raise ValueError("'search_type' parameter should be one of "
                                 "'query_then_fetch', 'query_and_fetch', "
                                 "'dfs_query_then_fetch', "
                                 "'dfs_query_and_fetch', 'count', 'scan'")

        _, data = yield from self.transport.perform_request(
            'POST',
            _make_path(index, doc_type, '_msearch'),
            params=params,
            body=self._bulk_body(body))

        return data

    @asyncio.coroutine
    def delete_by_query(self, index=None, doc_type=None, body=None, *,
                        allow_no_indices=default, analyzer=default,
                        consistency=default, default_operator=default,
                        df=default, expand_wildcards=default,
                        ignore_unavailable=default, q=default,
                        replication=default, routing=default,
                        source=default, timeout=default):
        """
        Delete documents from one or more indices and one or more types based
        on a query.
        """
        if index is None:
            index = '_all'

        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if analyzer is not default:
            params['analyzer'] = analyzer
        if default_operator is not default:
            if not isinstance(default_operator, str):
                raise TypeError("'default_operator' parameter is not a string")
            elif default_operator.upper() in ('AND', 'OR'):
                params['default_operator'] = default_operator.upper()
            else:
                raise ValueError("'default_operator' parameter should "
                                 "be one of 'AND', 'OR'")
        if df is not default:
            params['df'] = df
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if q is not default:
            params['q'] = q
        if routing is not default:
            params['routing'] = routing
        if source is not default:
            params['source'] = source
        if timeout is not default:
            params['timeout'] = timeout

        if consistency is not default:
            if not isinstance(consistency, str):
                raise TypeError("'consistency' parameter is not a string")
            elif consistency.lower() in ('one', 'quorum', 'all'):
                params['consistency'] = consistency.lower()
            else:
                raise ValueError("'consistency' parameter should be one of "
                                 "'one', 'quorum', 'all'")

        if replication is not default:
            if not isinstance(replication, str):
                raise TypeError("'replication' parameter is not a string")
            elif replication.lower() in ('async', 'sync'):
                params['replication'] = replication.lower()
            else:
                raise ValueError("'replication' parameter should be one of"
                                 " 'async', 'sync'")

        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not "
                                "a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be"
                                 " one of 'open', 'closed'")

        _, data = yield from self.transport.perform_request(
            'DELETE',
            _make_path(index, doc_type, '_query'),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def suggest(self, index, body, *,
                allow_no_indices=default, expand_wildcards=default,
                ignore_unavailable=default, preference=default,
                routing=default, source=default):
        """
        The suggest feature suggests similar looking terms based on a
        provided text by using a suggester.
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if preference is not default:
            params['preference'] = preference
        if routing is not default:
            params['routing'] = routing
        if source is not default:
            params['source'] = source

        _, data = yield from self.transport.perform_request(
            'POST',
            _make_path(index, '_suggest'),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def percolate(self, index, doc_type, doc_id=None, body=None, *,
                  allow_no_indices=default, expand_wildcards=default,
                  ignore_unavailable=default, percolate_format=default,
                  percolate_index=default, percolate_type=default,
                  preference=default, routing=default, version=default,
                  version_type=default):
        """
        The percolator allows to register queries against an index, and then
        send percolate requests which include a doc, and getting back the
        queries that match on that doc out of the set of registered queries.
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if percolate_format is not default:
            params['percolate_format'] = percolate_format
        if percolate_index is not default:
            params['percolate_index'] = percolate_index
        if percolate_type is not default:
            params['percolate_type'] = percolate_type
        if preference is not default:
            params['preference'] = preference
        if routing is not default:
            params['routing'] = routing
        if version is not default:
            params['version'] = int(version)
        if version_type is not default:
            if not isinstance(version_type, str):
                raise TypeError("'version_type' parameter is not a string")
            elif version_type.lower() in ('internal', 'external',
                                          'external_gt', 'external_gte',
                                          'force'):
                params['version_type'] = version_type.lower()
            else:
                raise ValueError("'version_type' parameter should be one of "
                                 "'internal', 'external', 'external_gt', "
                                 "'external_gte', 'force'")

        if bool(doc_id) == bool(body):
            raise ValueError('Please provide either doc_id or body')

        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path(index, doc_type, doc_id, '_percolate'),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def count_percolate(self, index, doc_type, doc_id=None, body=None, *,
                        allow_no_indices=default, expand_wildcards=default,
                        ignore_unavailable=default, percolate_format=default,
                        percolate_index=default, percolate_type=default,
                        preference=default, routing=default, version=default,
                        version_type=default):
        """
        The percolator allows to register queries against an index, and then
        send percolate requests which include a doc, and getting back the
        queries that match on that doc out of the set of registered queries.
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if percolate_format is not default:
            params['percolate_format'] = percolate_format
        if percolate_index is not default:
            params['percolate_index'] = percolate_index
        if percolate_type is not default:
            params['percolate_type'] = percolate_type
        if preference is not default:
            params['preference'] = preference
        if routing is not default:
            params['routing'] = routing
        if version is not default:
            params['version'] = int(version)
        if version_type is not default:
            if not isinstance(version_type, str):
                raise TypeError("'version_type' parameter is not a string")
            elif version_type.lower() in ('internal', 'external',
                                          'external_gt', 'external_gte',
                                          'force'):
                params['version_type'] = version_type.lower()
            else:
                raise ValueError("'version_type' parameter should be one of "
                                 "'internal', 'external', 'external_gt', "
                                 "'external_gte', 'force'")

        if bool(doc_id) == bool(body):
            raise ValueError('Please provide either doc_id or body')

        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path(index, doc_type, doc_id, '_percolate', 'count'),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def mpercolate(self, body, index=None, doc_type=None, *,
                   allow_no_indices=default, expand_wildcards=default,
                   ignore_unavailable=default):
        """
        The percolator allows to register queries against an index, and then
        send percolate requests which include a doc, and getting back the
        queries that match on that doc out of the set of registered queries.
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)

        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path(index, doc_type, '_mpercolate'),
            params=params,
            body=self._bulk_body(body))

        return data

    @asyncio.coroutine
    def mlt(self, index, doc_type, id, body=None, *,
            boost_terms=default, include=default, max_doc_freq=default,
            max_query_terms=default, max_word_length=default,
            min_doc_freq=default, min_term_freq=default,
            min_word_length=default, mlt_fields=default,
            percent_terms_to_match=default, routing=default,
            search_from=default, search_indices=default,
            search_query_hint=default, search_scroll=default,
            search_size=default, search_source=default,
            search_type=default, search_types=default, stop_words=default):
        """
        Get documents that are "like" a specified document.
        """
        params = {}
        if boost_terms is not default:
            params['boost_terms'] = boost_terms
        if include is not default:
            params['include'] = include
        if max_doc_freq is not default:
            params['max_doc_freq'] = max_doc_freq
        if max_query_terms is not default:
            params['max_query_terms'] = max_query_terms
        if max_word_length is not default:
            params['max_word_length'] = max_word_length
        if min_doc_freq is not default:
            params['min_doc_freq'] = min_doc_freq
        if min_term_freq is not default:
            params['min_term_freq'] = min_term_freq
        if min_word_length is not default:
            params['min_word_length'] = min_word_length
        if mlt_fields is not default:
            params['mlt_fields'] = mlt_fields
        if percent_terms_to_match is not default:
            params['percent_terms_to_match'] = percent_terms_to_match
        if routing is not default:
            params['routing'] = routing
        if search_from is not default:
            params['search_from'] = search_from
        if search_indices is not default:
            params['search_indices'] = search_indices
        if search_query_hint is not default:
            params['search_query_hint'] = search_query_hint
        if search_scroll is not default:
            params['search_scroll'] = search_scroll
        if search_size is not default:
            params['search_size'] = search_size
        if search_source is not default:
            params['search_source'] = search_source
        if search_type is not default:
            if not isinstance(search_type, str):
                raise TypeError("'search_type' parameter is not a string")
            elif search_type.lower() in ('query_then_fetch',
                                         'query_and_fetch',
                                         'dfs_query_then_fetch',
                                         'dfs_query_and_fetch',
                                         'count',
                                         'scan'):
                params['search_type'] = search_type.lower()
            else:
                raise ValueError("'search_type' parameter should be one of "
                                 "'query_then_fetch', 'query_and_fetch', "
                                 "'dfs_query_then_fetch', "
                                 "'dfs_query_and_fetch', 'count', 'scan'")
        if search_types is not default:
            params['search_types'] = search_types
        if stop_words is not default:
            params['stop_words'] = stop_words

        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path(index, doc_type, id, '_mlt'),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def termvector(self, index, doc_type, id, body=None, *,
                   field_statistics=default, fields=default,
                   offsets=default, parent=default, payloads=default,
                   positions=default, preference=default, routing=default,
                   term_statistics=default):
        """
        Returns information and statistics on terms in the fields of
        a particular document as stored in the index.
        """
        params = {}
        if field_statistics is not default:
            params['field_statistics'] = field_statistics
        if fields is not default:
            params['fields'] = fields
        if offsets is not default:
            params['offsets'] = offsets
        if parent is not default:
            params['parent'] = parent
        if payloads is not default:
            params['payloads'] = payloads
        if positions is not default:
            params['positions'] = positions
        if preference is not default:
            params['preference'] = preference
        if routing is not default:
            params['routing'] = routing
        if term_statistics is not default:
            params['term_statistics'] = term_statistics

        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path(index, doc_type, id, '_termvector'),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def mtermvectors(self, index=None, doc_type=None, body=None, *,
                     field_statistics=default, fields=default,
                     ids=default, offsets=default, parent=default,
                     payloads=default, positions=default,
                     preference=default, routing=default,
                     term_statistics=default):
        """
        Multi termvectors API allows to get multiple termvectors based on an
        index, type and id.
        """
        params = {}
        if field_statistics is not default:
            params['field_statistics'] = field_statistics
        if fields is not default:
            params['fields'] = fields
        if ids is not default:
            params['ids'] = ids
        if offsets is not default:
            params['offsets'] = offsets
        if parent is not default:
            params['parent'] = parent
        if payloads is not default:
            params['payloads'] = payloads
        if positions is not default:
            params['positions'] = positions
        if preference is not default:
            params['preference'] = preference
        if routing is not default:
            params['routing'] = routing
        if term_statistics is not default:
            params['term_statistics'] = term_statistics

        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path(index, doc_type, '_mtermvectors'),
            params=params, body=body)

        return data
    #
    # @asyncio.coroutine
    # def benchmark(self, index=None, doc_type=None, body=None, *,
    #               verbose=default):
    #     """
    #     The benchmark API provides a standard mechanism for submitting
    #     queries and measuring their performance relative to one another.
    #     """
    #     params = {}
    #     if verbose is not default:
    #         params['verbose'] = verbose
    #
    #     _, data = self.transport.perform_request(
    #         'PUT',
    #         _make_path(index, doc_type, '_bench'),
    #         params=params, body=body)
    #     return data
    #
    # @asyncio.coroutine
    # def abort_benchmark(self, name=None):
    #     """
    #     Aborts a running benchmark.
    #     `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/search-benchmark.html>`_
    #
    #     :param name: A benchmark name
    #     """
    #     _, data = yield from self.transport.perform_request(
    #         'POST', _make_path('_bench', 'abort', name))
    #     return data
    #
    # @asyncio.coroutine
    # def list_benchmarks(self, index=None, doc_type=None):
    #     """
    #     View the progress of long-running benchmarks.
    #     `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/search-benchmark.html>`_
    #
    #     :param index: A comma-separated list of index names; use `_all` or
    #         empty string to perform the operation on all indices
    #     :param doc_type: The name of the document type
    #     """
    #     _, data = yield from self.transport.perform_request(
    #         'GET', _make_path(index, doc_type, '_bench'))
    #     return data

    @asyncio.coroutine
    def put_script(self, lang, id, body):
        """
        Create a script in given language with specified ID.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-scripting.html>`_

        :param lang: Script language
        :param id: Script ID
        :param body: The document
        """
        _, data = yield from self.transport.perform_request(
            'PUT', _make_path('_scripts', lang, id), body=body)
        return data

    @asyncio.coroutine
    def get_script(self, lang, id):
        """
        Retrieve a script from the API.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-scripting.html>`_

        :param lang: Script language
        :param id: Script ID
        """
        _, data = yield from self.transport.perform_request(
            'GET', _make_path('_scripts', lang, id))
        return data

    @asyncio.coroutine
    def delete_script(self, lang, id):
        """
        Remove a stored script from elasticsearch.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-scripting.html>`_

        :param lang: Script language
        :param id: Script ID
        """
        _, data = yield from self.transport.perform_request(
            'DELETE', _make_path('_scripts', lang, id))
        return data

    @asyncio.coroutine
    def put_template(self, id, body):
        """
        Create a search template.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-template.html>`_

        :param id: Template ID
        :param body: The document
        """
        _, data = yield from self.transport.perform_request(
            'PUT', _make_path('_search', 'template', id),
            body=body)
        return data

    @asyncio.coroutine
    def get_template(self, id):
        """
        Retrieve a search template.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-template.html>`_

        :param id: Template ID
        """
        _, data = yield from self.transport.perform_request(
            'GET', _make_path('_search', 'template', id))
        return data

    @asyncio.coroutine
    def delete_template(self, id):
        """
        Delete a search template.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-template.html>`_

        :param id: Template ID
        """
        _, data = yield from self.transport.perform_request(
            'DELETE', _make_path('_search', 'template', id))
        return data
