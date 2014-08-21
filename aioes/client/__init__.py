import asyncio
import weakref
import json

from .indices import IndicesClient
from aioes.transport import Transport
from .utils import _make_path
from aioes.exception import NotFoundError, TransportError, SerializationError

default = object()


class Elasticsearch:
    def __init__(self, endpoints, *, loop=None, **kwargs):
        self._transport = Transport(endpoints, loop=loop, **kwargs)
        self._indices = weakref.ref(IndicesClient(self))
        # self._cluster = weakref.ref(ClusterClient(self))
        # self._cat = weakref.ref(CatClient(self))
        # self._nodes = weakref.ref(NodesClient(self))
        # self._snapshot = weakref.ref(SnapshotClient(self))

    @property
    def indices(self):
        return self._indices()

    @property
    def cluster(self):
        return self._cluster()

    @property
    def cat(self):
        return self._cat()

    @property
    def nodes(self):
        return self._nodes()

    @property
    def snapshot(self):
        return self._snapshot()

    def __repr__(self):
        pass

    def _bulk_body(self, body):
        # if not passed in a string, serialize items and join by newline
        if not isinstance(body, (str, bytes)):
            try:
                body = '\n'.join(map(json.dumps, body))
            except (ValueError, TypeError) as e:
                raise SerializationError(body, e)
        # bulk body must end with a newline
        if not body.endswith('\n'):
            body += '\n'

        return body

    def close(self):
        self._transport.close()

    @asyncio.coroutine
    def ping(self, *, pretty=default, format=default):
        """
        Returns True if the cluster is up, False otherwise.

        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        try:
            yield from self._transport.perform_request(
                'HEAD', '/', params=params)
        except TransportError:
            return False
        return True

    @asyncio.coroutine
    def info(self, *, pretty=default, format=default):
        """
        Get the basic info from the current cluster.

        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'GET', '/', params=params)
        return data

    @asyncio.coroutine
    def create(self, index, doc_type, body, id=None, *,
               consistency=default, parent=default, percolate=default,
               refresh=default, replication=default, routing=default,
               timeout=default, timestamp=default, ttl=default,
               version=default, version_type=default, pretty=default,
               format=default):
        """
        Adds a typed JSON document in a specific index, making it searchable.
        Behind the scenes this method calls index(..., op_type='create')
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-index_.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg id: Document ID
        :arg body: The document
        :arg consistency: Explicit write consistency setting for the operation
        :arg id: Specific document ID (when the POST method is used)
        :arg parent: ID of the parent document
        :arg percolate: Percolator queries to execute while indexing the document
        :arg refresh: Refresh the index after performing the operation
        :arg replication: Specific replication type (default: sync)
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg timestamp: Explicit timestamp for the document
        :arg ttl: Expiration time for the document
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if consistency is not default:
            params['consistency'] = consistency
        if parent is not default:
            params['parent'] = parent
        if percolate is not default:
            params['percolate'] = percolate
        if refresh is not default:
            params['refresh'] = refresh
        if replication is not default:
            params['replication'] = replication
        if routing is not default:
            params['routing'] = routing
        if timeout is not default:
            params['timeout'] = timeout
        if timestamp is not default:
            params['timestamp'] = timestamp
        if ttl is not default:
            params['ttl'] = ttl
        if version is not default:
            params['version'] = version
        if version_type is not default:
            params['version_type'] = version_type
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        return self.index(index, doc_type, body,
                          id=id, params=params, op_type='create')

    @asyncio.coroutine
    def index(self, index, doc_type, body, id=None, *,
              consistency=default, op_type=default, parent=default,
              refresh=default, replication=default, routing=default,
              timeout=default, timestamp=default, ttl=default,
              version=default, version_type=default, pretty=default,
              format=default):
        """
        Adds or updates a typed JSON document in a specific index, making it
        searchable.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-index_.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg body: The document
        :arg id: Document ID
        :arg consistency: Explicit write consistency setting for the operation
        :arg op_type: Explicit operation type (default: index)
        :arg parent: ID of the parent document
        :arg refresh: Refresh the index after performing the operation
        :arg replication: Specific replication type (default: sync)
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg timestamp: Explicit timestamp for the document
        :arg ttl: Expiration time for the document
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if consistency is not default:
            params['consistency'] = consistency
        if op_type is not default:
            params['op_type'] = op_type
        if parent is not default:
            params['parent'] = parent
        if refresh is not default:
            params['refresh'] = refresh
        if replication is not default:
            params['replication'] = replication
        if routing is not default:
            params['routing'] = routing
        if timeout is not default:
            params['timeout'] = timeout
        if timestamp is not default:
            params['timestamp'] = timestamp
        if ttl is not default:
            params['ttl'] = ttl
        if version is not default:
            params['version'] = version
        if version_type is not default:
            params['version_type'] = version_type
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'PUT' if id else 'POST',
            _make_path(index, doc_type, id),
            params=params,
            body=body)

        return data

    @asyncio.coroutine
    def exists(self, index, id, doc_type='_all', *, parent=default,
               preference=default, realtime=default, refresh=default,
               routing=default, pretty=default, format=default):
        """
        Returns a boolean indicating whether or not given document exists
        in Elasticsearch.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_

        :arg index: The name of the index
        :arg id: The document ID
        :arg doc_type: The type of the document (uses `_all` by default to
            fetch the first document matching the ID across all types)
        :arg parent: The ID of the parent document
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg realtime: Specify whether to perform the operation in realtime or
            search mode
        :arg refresh: Refresh the shard containing the document before
            performing the operation
        :arg routing: Specific routing value
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if parent is not default:
            params['parent'] = parent
        if preference is not default:
            params['preference'] = preference
        if realtime is not default:
            params['realtime'] = realtime
        if refresh is not default:
            params['refresh'] = refresh
        if routing is not default:
            params['routing'] = routing
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        try:
            yield from self._transport.perform_request(
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
            version_type=default, pretty=default, format=default):
        """
        Get a typed JSON document from the index based on its id.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_

        :arg index: The name of the index
        :arg id: The document ID
        :arg doc_type: The type of the document (uses `_all` by default to
            fetch the first document matching the ID across all types)
        :arg _source: True or false to return the _source field or not, or a
            list of fields to return
        :arg _source_exclude: A list of fields to exclude from the returned
            _source field
        :arg _source_include: A list of fields to extract and return from the
            _source field
        :arg fields: A comma-separated list of fields to return in the response
        :arg parent: The ID of the parent document
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg realtime: Specify whether to perform the operation in realtime or
            search mode
        :arg refresh: Refresh the shard containing the document before
            performing the operation
        :arg routing: Specific routing value
        :arg version: Explicit version number for concurrency control
        :arg version_type: Explicit version number for concurrency control
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
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
            params['realtime'] = realtime
        if refresh is not default:
            params['refresh'] = refresh
        if routing is not default:
            params['routing'] = routing
        if version is not default:
            params['version'] = version
        if version_type is not default:
            params['version_type'] = version_type
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
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
                   version_type=default, pretty=default, format=default):
        """
        Get the source of a document by it's index, type and id.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document (uses `_all` by default to
            fetch the first document matching the ID across all types)
        :arg id: The document ID
        :arg _source: True or false to return the _source field or not, or a
            list of fields to return
        :arg _source_exclude: A list of fields to exclude from the returned
            _source field
        :arg _source_include: A list of fields to extract and return from the
            _source field
        :arg parent: The ID of the parent document
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg realtime: Specify whether to perform the operation in realtime or search mode
        :arg refresh: Refresh the shard containing the document before
            performing the operation
        :arg routing: Specific routing value
        :arg version: Explicit version number for concurrency control
        :arg version_type: Explicit version number for concurrency control
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
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
            params['realtime'] = realtime
        if refresh is not default:
            params['refresh'] = refresh
        if routing is not default:
            params['routing'] = routing
        if version is not default:
            params['version'] = version
        if version_type is not default:
            params['version_type'] = version_type
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'GET',
            _make_path(index, doc_type, id, '_source'),
            params=params)

        return data

    @asyncio.coroutine
    def mget(self, body, index=None, doc_type=None, *,
             _source=default, _source_exclude=default,
             _source_include=default, fields=default, parent=default,
             preference=default, realtime=default, refresh=default,
             routing=default, pretty=default, format=default):
        """
        Get multiple documents based on an index, type (optional) and ids.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-multi-get.html>`_

        :arg body: Document identifiers; can be either `docs` (containing full
            document information) or `ids` (when index and type is provided in the URL.
        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg _source: True or false to return the _source field or not, or a
            list of fields to return
        :arg _source_exclude: A list of fields to exclude from the returned
            _source field
        :arg _source_include: A list of fields to extract and return from the
            _source field
        :arg fields: A comma-separated list of fields to return in the response
        :arg parent: The ID of the parent document
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg realtime: Specify whether to perform the operation in realtime or search mode
        :arg refresh: Refresh the shard containing the document before
            performing the operation
        :arg routing: Specific routing value
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
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
            params['realtime'] = realtime
        if refresh is not default:
            params['refresh'] = refresh
        if routing is not default:
            params['routing'] = routing
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'GET',
            _make_path(index, doc_type, '_mget'),
            params=params,
            body=body)

        return data

    @asyncio.coroutine
    def update(self, index, doc_type, id, body=None, *,
               consistency=default, fields=default, lang=default,
               parent=default, refresh=default, replication=default,
               retry_on_conflict=default, routing=default, script=default,
               timeout=default, timestamp=default, ttl=default,
               version=default, version_type=default, pretty=default,
               format=default):
        """
        Update a document based on a script or partial data provided.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-update.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg id: Document ID
        :arg body: The request definition using either `script` or partial `doc`
        :arg consistency: Explicit write consistency setting for the operation
        :arg fields: A comma-separated list of fields to return in the response
        :arg lang: The script language (default: mvel)
        :arg parent: ID of the parent document
        :arg refresh: Refresh the index after performing the operation
        :arg replication: Specific replication type (default: sync)
        :arg retry_on_conflict: Specify how many times should the operation be
            retried when a conflict occurs (default: 0)
        :arg routing: Specific routing value
        :arg script: The URL-encoded script definition (instead of using request body)
        :arg timeout: Explicit operation timeout
        :arg timestamp: Explicit timestamp for the document
        :arg ttl: Expiration time for the document
        :arg version: Explicit version number for concurrency control
        :arg version_type: Explicit version number for concurrency control
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if consistency is not default:
            params['consistency'] = consistency
        if fields is not default:
            params['fields'] = fields
        if lang is not default:
            params['lang'] = lang
        if parent is not default:
            params['parent'] = parent
        if refresh is not default:
            params['refresh'] = refresh
        if replication is not default:
            params['replication'] = replication
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
            params['version'] = version
        if version_type is not default:
            params['version_type'] = version_type
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'POST',
            _make_path(index, doc_type, id, '_update'),
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
               timeout=default, version=default, pretty=default,
               format=default):
        """
        Execute a search query and get back search hits that match the query.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-search.html>`_

        :arg index: A comma-separated list of index names to search; use `_all`
            or empty string to perform the operation on all indices
        :arg doc_type: A comma-separated list of document types to search;
            leave empty to perform the operation on all types
        :arg body: The search definition using the Query DSL
        :arg _source: True or false to return the _source field or not, or a
            list of fields to return
        :arg _source_exclude: A list of fields to exclude from the returned
            _source field
        :arg _source_include: A list of fields to extract and return from the
            _source field
        :arg analyze_wildcard: Specify whether wildcard and prefix queries
            should be analyzed (default: false)
        :arg analyzer: The analyzer to use for the query string
        :arg default_operator: The default operator for query string query (AND
            or OR) (default: OR)
        :arg df: The field to use as default where no field prefix is given in
            the query string
        :arg explain: Specify whether to return detailed information about
            score computation as part of a hit
        :arg fields: A comma-separated list of fields to return as part of a hit
        :arg indices_boost: Comma-separated list of index boosts
        :arg lenient: Specify whether format-based query failures (such as
            providing text to a numeric field) should be ignored
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg lowercase_expanded_terms: Specify whether query terms should be lowercased
        :arg from\_: Starting offset (default: 0)
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg routing: A comma-separated list of specific routing values
        :arg scroll: Specify how long a consistent view of the index should be
            maintained for scrolled search
        :arg search_type: Search operation type
        :arg size: Number of hits to return (default: 10)
        :arg sort: A comma-separated list of <field>:<direction> pairs
        :arg source: The URL-encoded request definition using the Query DSL
            (instead of using request body)
        :arg stats: Specific 'tag' of the request for logging and statistical purposes
        :arg suggest_field: Specify which field to use for suggestions
        :arg suggest_mode: Specify suggest mode (default: missing)
        :arg suggest_size: How many suggestions to return in response
        :arg suggest_text: The source text for which the suggestions should be returned
        :arg timeout: Explicit operation timeout
        :arg version: Specify whether to return document version as part of a hit
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if _source is not default:
            params['_source'] = _source
        if _source_exclude is not default:
            params['_source_exclude'] = _source_exclude
        if _source_include is not default:
            params['_source_include'] = _source_include
        if analyze_wildcard is not default:
            params['analyze_wildcard'] = analyze_wildcard
        if analyzer is not default:
            params['analyzer'] = analyzer
        if default_operator is not default:
            params['default_operator'] = default_operator
        if df is not default:
            params['df'] = df
        if explain is not default:
            params['explain'] = explain
        if fields is not default:
            params['fields'] = fields
        if indices_boost is not default:
            params['indices_boost'] = indices_boost
        if lenient is not default:
            params['lenient'] = lenient
        if allow_no_indices is not default:
            params['allow_no_indices'] = allow_no_indices
        if expand_wildcards is not default:
            params['expand_wildcards'] = expand_wildcards
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = ignore_unavailable
        if lowercase_expanded_terms is not default:
            params['lowercase_expanded_terms'] = lowercase_expanded_terms
        # from is a reserved word so it cannot be used, use from_ instead
        if from_ is not default:
            params['from'] = from_
        if preference is not default:
            params['preference'] = preference
        if q is not default:
            params['q'] = q
        if routing is not default:
            params['routing'] = routing
        if scroll is not default:
            params['scroll'] = scroll
        if search_type is not default:
            params['search_type'] = search_type
        if size is not default:
            params['size'] = size
        if sort is not default:
            params['sort'] = sort
        if source is not default:
            params['source'] = source
        if stats is not default:
            params['stats'] = stats
        if suggest_field is not default:
            params['suggest_field'] = suggest_field
        if suggest_mode is not default:
            params['suggest_mode'] = suggest_mode
        if suggest_size is not default:
            params['suggest_size'] = suggest_size
        if suggest_text is not default:
            params['suggest_text'] = suggest_text
        if timeout is not default:
            params['timeout'] = timeout
        if version is not default:
            params['version'] = version
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        if doc_type and not index:
            index = '_all'

        _, data = yield from self._transport.perform_request(
            'GET',
            _make_path(index, doc_type, '_search'),
            params=params,
            body=body)

        return data

    @asyncio.coroutine
    def search_shards(self, index=None, doc_type=None, *,
                      allow_no_indices=default, expand_wildcards=default,
                      ignore_unavailable=default, local=default,
                      preference=default, routing=default, pretty=default,
                      format=default):
        """
        The search shards api returns the indices and shards that a search
        request would be executed against. This can give useful feedback for working
        out issues or planning optimizations with routing and shard preferences.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/search-shards.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both. (default: '"open"')
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg routing: Specific routing value
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = allow_no_indices
        if expand_wildcards is not default:
            params['expand_wildcards'] = expand_wildcards
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = ignore_unavailable
        if local is not default:
            params['local'] = local
        if preference is not default:
            params['preference'] = preference
        if routing is not default:
            params['routing'] = routing
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
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
                        search_type=default, pretty=default,
                        format=default):
        """
        A query that accepts a query template and a map of key/value pairs to
        fill in template parameters.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/query-dsl-template-query.html>`_

        :arg index: A comma-separated list of index names to search; use `_all`
            or empty string to perform the operation on all indices
        :arg doc_type: A comma-separated list of document types to search; leave
            empty to perform the operation on all types
        :arg body: The search definition template and its params
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg routing: A comma-separated list of specific routing values
        :arg scroll: Specify how long a consistent view of the index should be
            maintained for scrolled search
        :arg search_type: Search operation type
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = allow_no_indices
        if expand_wildcards is not default:
            params['expand_wildcards'] = expand_wildcards
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = ignore_unavailable
        if preference is not default:
            params['preference'] = preference
        if routing is not default:
            params['routing'] = routing
        if scroll is not default:
            params['scroll'] = scroll
        if search_type is not default:
            params['search_type'] = search_type
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
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
                source=default, pretty=default, format=default):
        """
        The explain api computes a score explanation for a query and a specific
        document. This can give useful feedback whether a document matches or
        didn't match a specific query.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-explain.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg id: The document ID
        :arg body: The query definition using the Query DSL
        :arg _source: True or false to return the _source field or not, or a
            list of fields to return
        :arg _source_exclude: A list of fields to exclude from the returned
            _source field
        :arg _source_include: A list of fields to extract and return from the
            _source field
        :arg analyze_wildcard: Specify whether wildcards and prefix queries in
            the query string query should be analyzed (default: false)
        :arg analyzer: The analyzer for the query string query
        :arg default_operator: The default operator for query string query (AND
            or OR), (default: OR)
        :arg df: The default field for query string query (default: _all)
        :arg fields: A comma-separated list of fields to return in the response
        :arg lenient: Specify whether format-based query failures (such as
            providing text to a numeric field) should be ignored
        :arg lowercase_expanded_terms: Specify whether query terms should be lowercased
        :arg parent: The ID of the parent document
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg routing: Specific routing value
        :arg source: The URL-encoded query definition (instead of using the
            request body)
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if _source is not default:
            params['_source'] = _source
        if _source_exclude is not default:
            params['_source_exclude'] = _source_exclude
        if _source_include is not default:
            params['_source_include'] = _source_include
        if analyze_wildcard is not default:
            params['analyze_wildcard'] = analyze_wildcard
        if analyzer is not default:
            params['analyzer'] = analyzer
        if default_operator is not default:
            params['default_operator'] = default_operator
        if df is not default:
            params['df'] = df
        if fields is not default:
            params['fields'] = fields
        if lenient is not default:
            params['lenient'] = lenient
        if lowercase_expanded_terms is not default:
            params['lowercase_expanded_terms'] = lowercase_expanded_terms
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
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'GET',
            _make_path(index, doc_type, id, '_explain'),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def scroll(self, scroll_id, *, scroll=default, pretty=default,
               format=default):
        """
        Scroll a search request created by specifying the scroll parameter.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-request-scroll.html>`_

        :arg scroll_id: The scroll ID
        :arg scroll: Specify how long a consistent view of the index should be
            maintained for scrolled search
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if scroll is not default:
            params['scroll'] = scroll
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'GET',
            '/_search/scroll',
            params=params, body=scroll_id)

        return data

    @asyncio.coroutine
    def clear_scroll(self, scroll_id=None, body=None, *,
                     pretty=default, format=default):
        """
        Clear the scroll request created by specifying the scroll parameter to
        search.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-request-scroll.html>`_

        :arg scroll_id: The scroll ID or a list of scroll IDs
        :arg body: A comma-separated list of scroll IDs to clear if none was
            specified via the scroll_id parameter
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self.transport.perform_request(
            'DELETE',
            _make_path('_search', 'scroll', scroll_id),
            body=body, params=params)

        return data

    @asyncio.coroutine
    def delete(self, index, doc_type, id, *,
               consistency=default, parent=default, refresh=default,
               replication=default, routing=default, timeout=default,
               version=default, version_type=default, pretty=default,
               format=default):
        """
        Delete a typed JSON document from a specific index based on its id.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-delete.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg id: The document ID
        :arg consistency: Specific write consistency setting for the operation
        :arg parent: ID of parent document
        :arg refresh: Refresh the index after performing the operation
        :arg replication: Specific replication type (default: sync)
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if consistency is not default:
            params['consistency'] = consistency
        if replication is not default:
            params['replication'] = replication
        if timeout is not default:
            params['timeout'] = timeout
        if parent is not default:
            params['parent'] = parent
        if refresh is not default:
            params['refresh'] = refresh
        if routing is not default:
            params['routing'] = routing
        if version is not default:
            params['version'] = version
        if version_type is not default:
            params['version_type'] = version_type
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'DELETE',
            _make_path(index, doc_type, id),
            params=params)

        return data

    @asyncio.coroutine
    def count(self, index=None, doc_type=None, body=None, *,
              allow_no_indices=default, expand_wildcards=default,
              ignore_unavailable=default, min_score=default,
              preference=default, q=default, routing=default,
              source=default, pretty=default, format=default):
        """
        Execute a query and get the number of matches for that query.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-count.html>`_

        :arg index: A comma-separated list of indices to restrict the results
        :arg doc_type: A comma-separated list of types to restrict the results
        :arg body: A query to restrict the results (optional)
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg min_score: Include only documents with a specific `_score` value in the result
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg routing: Specific routing value
        :arg source: The URL-encoded query definition (instead of using the request body)
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = allow_no_indices
        if expand_wildcards is not default:
            params['expand_wildcards'] = expand_wildcards
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = ignore_unavailable
        if min_score is not default:
            params['min_score'] = min_score
        if preference is not default:
            params['preference'] = preference
        if q is not default:
            params['q'] = q
        if routing is not default:
            params['routing'] = routing
        if source is not default:
            params['source'] = source
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'POST',
            _make_path(index, doc_type, '_count'),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def bulk(self, body, index=None, doc_type=None, *,
             consistency=default, refresh=default, routing=default,
             replication=default, timeout=default, pretty=default,
             format=default):
        """
        Perform many index/delete operations in a single API call.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-bulk.html>`_

        See the :func:`~elasticsearch.helpers.bulk` helper function for a more
        friendly API.

        :arg body: The operation definition and data (action-data pairs), as
            either a newline separated string, or a sequence of dicts to
            serialize (one per row).
        :arg index: Default index for items which don't provide one
        :arg doc_type: Default document type for items which don't provide one
        :arg consistency: Explicit write consistency setting for the operation
        :arg refresh: Refresh the index after performing the operation
        :arg routing: Specific routing value
        :arg replication: Explicitly set the replication type (default: sync)
        :arg timeout: Explicit operation timeout
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if consistency is not default:
            params['consistency'] = consistency
        if refresh is not default:
            params['refresh'] = refresh
        if routing is not default:
            params['routing'] = routing
        if replication is not default:
            params['replication'] = replication
        if timeout is not default:
            params['timeout'] = timeout
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'POST',
            _make_path(index, doc_type, '_bulk'),
            params=params,
            body=self._bulk_body(body))

        return data

    @asyncio.coroutine
    def msearch(self, body, index=None, doc_type=None, *,
                search_type=default, pretty=default, format=default):
        """
        Execute several search requests within the same API.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-multi-search.html>`_

        :arg body: The request definitions (metadata-search request definition
            pairs), as either a newline separated string, or a sequence of
            dicts to serialize (one per row).
        :arg index: A comma-separated list of index names to use as default
        :arg doc_type: A comma-separated list of document types to use as default
        :arg search_type: Search operation type
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if search_type is not default:
            params['search_type'] = search_type
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'GET',
            _make_path(index, doc_type, '_msearch'),
            params=params,
            body=self._bulk_body(body))

        return data

    @asyncio.coroutine
    def delete_by_query(self, index, doc_type=None, body=None, *,
                        allow_no_indices=default, analyzer=default,
                        consistency=default, default_operator=default,
                        df=default, expand_wildcards=default,
                        ignore_unavailable=default, q=default,
                        replication=default, routing=default,
                        source=default, timeout=default, pretty=default,
                        format=default):
        """
        Delete documents from one or more indices and one or more types based on a query.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-delete-by-query.html>`_

        :arg index: A comma-separated list of indices to restrict the operation;
            use `_all` to perform the operation on all indices
        :arg doc_type: A comma-separated list of types to restrict the operation
        :arg body: A query to restrict the operation specified with the Query
            DSL
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg analyzer: The analyzer to use for the query string
        :arg consistency: Specific write consistency setting for the operation
        :arg default_operator: The default operator for query string query (AND
            or OR), default u'OR'
        :arg df: The field to use as default where no field prefix is given in
            the query string
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default u'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg q: Query in the Lucene query string syntax
        :arg replication: Specific replication type, default u'sync'
        :arg routing: Specific routing value
        :arg source: The URL-encoded query definition (instead of using the
            request body)
        :arg timeout: Explicit operation timeout
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = allow_no_indices
        if analyzer is not default:
            params['analyzer'] = analyzer
        if consistency is not default:
            params['consistency'] = consistency
        if default_operator is not default:
            params['default_operator'] = default_operator
        if df is not default:
            params['df'] = df
        if expand_wildcards is not default:
            params['expand_wildcards'] = expand_wildcards
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = ignore_unavailable
        if q is not default:
            params['q'] = q
        if replication is not default:
            params['replication'] = replication
        if routing is not default:
            params['routing'] = routing
        if source is not default:
            params['source'] = source
        if timeout is not default:
            params['timeout'] = timeout
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'DELETE',
            _make_path(index, doc_type, '_query'),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def suggest(self, body, index=None, *,
                allow_no_indices=default, expand_wildcards=default,
                ignore_unavailable=default, preference=default,
                routing=default, source, pretty=default, format=default):
        """
        The suggest feature suggests similar looking terms based on a provided
        text by using a suggester.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-search.html>`_

        :arg index: A comma-separated list of index names to restrict the operation;
            use `_all` or empty string to perform the operation on all indices
        :arg body: The request definition
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg routing: Specific routing value
        :arg source: The URL-encoded request definition (instead of using request body)
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = allow_no_indices
        if expand_wildcards is not default:
            params['expand_wildcards'] = expand_wildcards
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = ignore_unavailable
        if preference is not default:
            params['preference'] = preference
        if routing is not default:
            params['routing'] = routing
        if source is not default:
            params['source'] = source
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'POST',
            _make_path(index, '_suggest'),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def percolate(self, index, doc_type, id=None, body=None, *,
                  allow_no_indices=default, expand_wildcards=default,
                  ignore_unavailable=default, percolate_format=default,
                  percolate_index=default, percolate_type=default,
                  preference=default, routing=default, version=default,
                  version_type=default, pretty=default, format=default):
        """
        The percolator allows to register queries against an index, and then
        send percolate requests which include a doc, and getting back the
        queries that match on that doc out of the set of registered queries.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-percolate.html>`_

        :arg index: The index of the document being percolated.
        :arg doc_type: The type of the document being percolated.
        :arg id: Substitute the document in the request body with a document
            that is known by the specified id. On top of the id, the index and
            type parameter will be used to retrieve the document from within the
            cluster.
        :arg body: The percolator request definition using the percolate DSL
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg percolate_format: Return an array of matching query IDs instead of
            objects
        :arg percolate_index: The index to percolate the document into. Defaults
            to index.
        :arg percolate_type: The type to percolate document into. Defaults to
            type.
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg routing: A comma-separated list of specific routing values
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = allow_no_indices
        if expand_wildcards is not default:
            params['expand_wildcards'] = expand_wildcards
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = ignore_unavailable
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
            params['version'] = version
        if version_type is not default:
            params['version_type'] = version_type
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'GET',
            _make_path(index, doc_type, id, '_percolate'),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def mpercolate(self, body, index=None, doc_type=None, *,
                   allow_no_indices=default, expand_wildcards=default,
                   ignore_unavailable=default, pretty=default, format=default):
        """
        The percolator allows to register queries against an index, and then
        send percolate requests which include a doc, and getting back the
        queries that match on that doc out of the set of registered queries.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-percolate.html>`_

        :arg index: The index of the document being count percolated to use as
            default
        :arg doc_type: The type of the document being percolated to use as
            default.
        :arg body: The percolate request definitions (header & body pair),
            separated by newlines
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = allow_no_indices
        if expand_wildcards is not default:
            params['expand_wildcards'] = expand_wildcards
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = ignore_unavailable
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'GET',
            _make_path(index, doc_type, '_mpercolate'),
            params=params,
            body=self._bulk_body(body))

        return data

    @asyncio.coroutine
    def count_percolate(self, index, doc_type, id=None, body=None, *,
                        allow_no_indices=default, expand_wildcards=default,
                        ignore_unavailable=default, percolate_index=default,
                        percolate_type=default, preference=default,
                        routing=default, version=default, version_type=default,
                        pretty=default, format=default):
        """
        The percolator allows to register queries against an index, and then
        send percolate requests which include a doc, and getting back the
        queries that match on that doc out of the set of registered queries.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-percolate.html>`_

        :arg index: The index of the document being count percolated.
        :arg doc_type: The type of the document being count percolated.
        :arg id: Substitute the document in the request body with a document
            that is known by the specified id. On top of the id, the index and
            type parameter will be used to retrieve the document from within the
            cluster.
        :arg body: The count percolator request definition using the percolate
            DSL
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg percolate_index: The index to count percolate the document into.
            Defaults to index.
        :arg percolate_type: The type to count percolate document into. Defaults
            to type.
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg routing: A comma-separated list of specific routing values
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = allow_no_indices
        if expand_wildcards is not default:
            params['expand_wildcards'] = expand_wildcards
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = ignore_unavailable
        if percolate_index is not default:
            params['percolate_index'] = percolate_index
        if percolate_type is not default:
            params['percolate_type'] = percolate_type
        if preference is not default:
            params['preference'] = preference
        if routing is not default:
            params['routing'] = routing
        if version is not default:
            params['version'] = version
        if version_type is not default:
            params['version_type'] = version_type
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'GET',
            _make_path(index, doc_type, id, '_percolate', 'count'),
            params=params, body=body)

        return data

    @query_params('')
    def mlt(self, index, doc_type, id, body=None, *,
            boost_terms=default, include=default, max_doc_freq=default,
            max_query_terms=default, max_word_length=default,
            min_doc_freq=default, min_term_freq=default,
            min_word_length=default, mlt_fields=default,
            percent_terms_to_match=default, routing=default,
            search_from=default, search_indices=default,
            search_query_hint=default, search_scroll=default,
            search_size=default, search_source=default,
            search_type=default, search_types=default, stop_words=default,
            pretty=default, format=default):
        """
        Get documents that are "like" a specified document.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-more-like-this.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document (use `_all` to fetch the first
            document matching the ID across all types)
        :arg id: The document ID
        :arg body: A specific search request definition
        :arg boost_terms: The boost factor
        :arg include: Whether to include the queried document from the response
        :arg max_doc_freq: The word occurrence frequency as count: words with
            higher occurrence in the corpus will be ignored
        :arg max_query_terms: The maximum query terms to be included in the generated query
        :arg max_word_length: The minimum length of the word: longer words will be ignored
        :arg min_doc_freq: The word occurrence frequency as count: words with
            lower occurrence in the corpus will be ignored
        :arg min_term_freq: The term frequency as percent: terms with lower
            occurence in the source document will be ignored
        :arg min_word_length: The minimum length of the word: shorter words will be ignored
        :arg mlt_fields: Specific fields to perform the query against
        :arg percent_terms_to_match: How many terms have to match in order to
            consider the document a match (default: 0.3)
        :arg routing: Specific routing value
        :arg search_from: The offset from which to return results
        :arg search_indices: A comma-separated list of indices to perform the
            query against (default: the index containing the document)
        :arg search_query_hint: The search query hint
        :arg search_scroll: A scroll search request definition
        :arg search_size: The number of documents to return (default: 10)
        :arg search_source: A specific search request definition (instead of
            using the request body)
        :arg search_type: Specific search type (eg. `dfs_then_fetch`, `count`, etc)
        :arg search_types: A comma-separated list of types to perform the query
            against (default: the same type as the document)
        :arg stop_words: A list of stop words to be ignored
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
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
            params['search_type'] = search_type
        if search_types is not default:
            params['search_types'] = search_types
        if stop_words is not default:
            params['stop_words'] = stop_words
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'GET',
            _make_path(index, doc_type, id, '_mlt'),
            params=params, body=body)

        return data

    @query_params('')
    def termvector(self, index, doc_type, id, body=None, *,
                   field_statistics=default, fields=default,
                   offsets=default, parent=default, payloads=default,
                   positions=default, preference=default, routing=default,
                   term_statistics=default, pretty=default, format=default):
        """
        Added in 1.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/search-termvectors.html>`_

        :arg index: The index in which the document resides.
        :arg doc_type: The type of the document.
        :arg id: The id of the document.
        :arg body: Define parameters. See documentation.
        :arg field_statistics: Specifies if document count, sum of document
            frequencies and sum of total term frequencies should be returned.,
            default True
        :arg fields: A comma-separated list of fields to return.
        :arg offsets: Specifies if term offsets should be returned., default
            True
        :arg parent: Parent id of documents.
        :arg payloads: Specifies if term payloads should be returned., default
            True
        :arg positions: Specifies if term positions should be returned., default
            True
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random).
        :arg routing: Specific routing value.
        :arg term_statistics: Specifies if total term frequency and document
            frequency should be returned., default False
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
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
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
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
                     term_statistics=default, pretty=default,
                     format=default):
        """
        Multi termvectors API allows to get multiple termvectors based on an
        index, type and id.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/docs-multi-termvectors.html>`_

        :arg index: The index in which the document resides.
        :arg doc_type: The type of the document.
        :arg body: Define ids, parameters or a list of parameters per document
            here. You must at least provide a list of document ids. See
            documentation.
        :arg field_statistics: Specifies if document count, sum of document
            frequencies and sum of total term frequencies should be returned.
            Applies to all returned documents unless otherwise specified in body
            "params" or "docs"., default True
        :arg fields: A comma-separated list of fields to return. Applies to all
            returned documents unless otherwise specified in body "params" or
            "docs".
        :arg ids: A comma-separated list of documents ids. You must define ids
            as parameter or set "ids" or "docs" in the request body
        :arg offsets: Specifies if term offsets should be returned. Applies to
            all returned documents unless otherwise specified in body "params"
            or "docs"., default True
        :arg parent: Parent id of documents. Applies to all returned documents
            unless otherwise specified in body "params" or "docs".
        :arg payloads: Specifies if term payloads should be returned. Applies to
            all returned documents unless otherwise specified in body "params"
            or "docs"., default True
        :arg positions: Specifies if term positions should be returned. Applies
            to all returned documents unless otherwise specified in body
            "params" or "docs"., default True
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random) .Applies to all returned documents
            unless otherwise specified in body "params" or "docs".
        :arg routing: Specific routing value. Applies to all returned documents
            unless otherwise specified in body "params" or "docs".
        :arg term_statistics: Specifies if total term frequency and document
            frequency should be returned. Applies to all returned documents
            unless otherwise specified in body "params" or "docs"., default
            False
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
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
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'GET',
            _make_path(index, doc_type, '_mtermvectors'),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def benchmark(self, index=None, doc_type=None, body=None, *,
                  verbose=default, pretty=default, format=default):
        """
        The benchmark API provides a standard mechanism for submitting queries
        and measuring their performance relative to one another.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/search-benchmark.html>`_

        :arg index: A comma-separated list of index names; use `_all` or empty
            string to perform the operation on all indices
        :arg doc_type: The name of the document type
        :arg body: The search definition using the Query DSL
        :arg verbose: Specify whether to return verbose statistics about each
            iteration (default: false)
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if verbose is not default:
            params['verbose'] = verbose
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = self._transport.perform_request(
            'PUT',
            _make_path(index, doc_type, '_bench'),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def abort_benchmark(self, name=None, *, pretty=default,
                        format=default):
        """
        Aborts a running benchmark.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/search-benchmark.html>`_

        :arg name: A benchmark name
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'POST',
            _make_path('_bench', 'abort', name),
            params=params)

        return data

    @asyncio.coroutine
    def list_benchmarks(self, index=None, doc_type=None, *,
                        pretty=default, format=default):
        """
        View the progress of long-running benchmarks.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/search-benchmark.html>`_

        :arg index: A comma-separated list of index names; use `_all` or empty
            string to perform the operation on all indices
        :arg doc_type: The name of the document type
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'GET',
            _make_path(index, doc_type, '_bench'),
            params=params)

        return data

    @asyncio.coroutine
    def put_script(self, lang, id, body, *, pretty=default,
                   format=default):
        """
        Create a script in given language with specified ID.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-scripting.html>`_

        :arg lang: Script language
        :arg id: Script ID
        :arg body: The document
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'PUT',
            _make_path('_scripts', lang, id),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def get_script(self, lang, id, *, pretty=default, format=default):
        """
        Retrieve a script from the API.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-scripting.html>`_

        :arg lang: Script language
        :arg id: Script ID
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'GET',
            _make_path('_scripts', lang, id),
            params=params)

        return data

    @asyncio.coroutine
    def delete_script(self, lang, id, *, pretty=default, format=default):
        """
        Remove a stored script from elasticsearch.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-scripting.html>`_

        :arg lang: Script language
        :arg id: Script ID
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'DELETE',
            _make_path('_scripts', lang, id),
            params=params)

        return data

    @asyncio.coroutine
    def put_template(self, id, body, *, pretty=default, format=default):
        """
        Create a search template.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-template.html>`_

        :arg id: Template ID
        :arg body: The document
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'PUT',
            _make_path('_search', 'template', id),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def get_template(self, id, body=None, *, pretty=default, format=default):
        """
        Retrieve a search template.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-template.html>`_

        :arg id: Template ID
        :arg body: The document
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self._transport.perform_request(
            'GET',
            _make_path('_search', 'template', id),
            params=params, body=body)

        return data

    @asyncio.coroutine
    def delete_template(self, id=None, *, pretty=default, format=default):
        """
        Delete a search template.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-template.html>`_

        :arg id: Template ID
        :arg pretty:
        :arg format: Format of the output, default 'detailed'
        """
        params = {}
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self.transport.perform_request(
            'DELETE',
            _make_path('_search', 'template', id),
            params=params)

        return data

