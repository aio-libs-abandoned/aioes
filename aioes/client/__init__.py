import asyncio
import weakref

from .indices import IndicesClient
from aioes.transport import Transport
from .utils import _make_path
from aioes.exception import NotFoundError

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

    def close(self):
        self._transport.close()

    def ping(self):
        pass

    def info(self):
        pass

    def create(self):
        pass

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
        if refresh is not default:
            params['refresh'] = refresh
        if preference is not default:
            params['preference'] = preference
        if routing is not default:
            params['routing'] = routing
        if realtime is not default:
            params['realtime'] = realtime
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        try:
            yield from self._transport.perform_request('HEAD', _make_path(index, doc_type, id), params=params)
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
        if refresh is not default:
            params['refresh'] = refresh
        if preference is not default:
            params['preference'] = preference
        if routing is not default:
            params['routing'] = routing
        if realtime is not default:
            params['realtime'] = realtime
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

    def get_source(self):
        pass

    def mget(self):
        pass

    def update(self):
        pass

    def search(self):
        pass

    def search_shards(self):
        pass

    def search_template(self):
        pass

    def explain(self):
        pass

    def scroll(self):
        pass

    def clear_scroll(self):
        pass

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

        _, data = yield from self._transport.perform_request('DELETE', _make_path(index, doc_type, id), params=params)
        return data

    def count(self):
        pass

    def bulk(self):
        pass

    def msearch(self):
        pass

    def delete_by_query(self):
        pass

    def suggest(self):
        pass

    def percolate(self):
        pass

    def mpercolate(self):
        pass

    def count_percolate(self):
        pass

    def mlt(self):
        pass

    def termvector(self):
        pass

    def mtermvectors(self):
        pass

    def benchmark(self):
        pass

    def abort_benchmark(self):
        pass

    def list_enchmark(self):
        pass

    def put_script(self):
        pass

    def get_script(self):
        pass

    def delete_script(self):
        pass

    def put_template(self):
        pass

    def get_template(self):
        pass

    def delete_template(self):
        pass
