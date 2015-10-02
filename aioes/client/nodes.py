import asyncio

from .utils import NamespacedClient
from .utils import _make_path

default = object()


def _decode_text(s):
    return s


class NodesClient(NamespacedClient):

    @asyncio.coroutine
    def info(self, node_id=None, metric=None, *,
             flat_settings=default, human=default):
        """
        The cluster nodes info API allows to retrieve one or more (or all) of
        the cluster nodes information.
        """
        params = {}
        if flat_settings is not default:
            params['flat_settings'] = bool(flat_settings)
        if human is not default:
            params['human'] = bool(human)
        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path('_nodes', node_id, metric),
            params=params)
        return data

    @asyncio.coroutine
    def shutdown(self, node_id=None, *, delay=default, exit=default):
        """
        The nodes shutdown API allows to shutdown one or more (or all) nodes in
        the cluster.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-nodes-shutdown.html>`_

        :arg node_id: A comma-separated list of node IDs or names to perform
            the operation on; use `_local` to perform the operation on
            the node you're connected to, leave empty to perform the operation
            on all nodes
        :arg delay: Set the delay for the operation (default: 1s)
        :arg exit: Exit the JVM as well (default: true)
        """
        params = {}

        if delay is not default:
            params['delay'] = delay
        if exit is not default:
            params['exit'] = bool(exit)

        _, data = yield from self.transport.perform_request(
            'POST', _make_path('_cluster', 'nodes', node_id, '_shutdown'),
            params=params
        )
        return data

    @asyncio.coroutine
    def stats(self, node_id=None, metric=None, index_metric=None, *,
              completion_fields=default, fielddata_fields=default,
              fields=default, groups=default, human=default, level=default,
              types=default):
        """
        The cluster nodes stats API allows to retrieve one or more (or all) of
        the cluster nodes statistics.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-nodes-stats.html>`_

        :arg node_id: A comma-separated list of node IDs or names to limit the
            returned information; use `_local` to return information from the
            node you're connecting to, leave empty to get information from all
            nodes
        :arg metric: Limit the information returned to the specified metrics.
            Possible options are: "_all", "breaker", "fs", "http", "indices",
            "jvm", "network", "os", "process", "thread_pool", "transport"
        :arg index_metric: Limit the information returned for `indices` metric
            to the specific index metrics. Isn't used if `indices` (or `all`)
            metric isn't specified. Possible options are: "_all", "completion",
            "docs", "fielddata", "filter_cache", "flush", "get", "id_cache",
            "indexing", "merge", "percolate", "refresh", "search", "segments",
            "store", "warmer"
        :arg completion_fields: A comma-separated list of fields
            for `fielddata` and `suggest` index metric (supports wildcards)
        :arg fielddata_fields: A comma-separated list of fields for `fielddata`
            index metric (supports wildcards)
        :arg fields: A comma-separated list of fields for `fielddata` and
            `completion` index metric (supports wildcards)
        :arg groups: A comma-separated list of search groups for `search` index
            metric
        :arg human: Whether to return time and byte values in human-readable
            format., default False
        :arg level: Return indices stats aggregated at node, index or shard
            level, default 'node'
        :arg types: A comma-separated list of document types for the `indexing`
            index metric
        """
        params = {}

        if completion_fields is not default:
            params['completion_fields'] = completion_fields
        if fielddata_fields is not default:
            params['fielddata_fields'] = fielddata_fields
        if fields is not default:
            params['fields'] = fields
        if groups is not default:
            params['groups'] = groups
        if human is not default:
            params['human'] = bool(human)
        if level is not default:
            params['level'] = level
        if types is not default:
            params['types'] = types

        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path('_nodes', node_id, 'stats', metric, index_metric),
            params=params
        )
        return data

    @asyncio.coroutine
    def hot_threads(self, node_id=None, *, type_=default, interval=default,
                    snapshots=default, threads=default):
        """
        An API allowing to get the current hot threads on each node
        in the cluster.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-nodes-hot-threads.html>`_

        :arg node_id: A comma-separated list of node IDs or names to limit the
            returned information; use `_local` to return information from the
            node you're connecting to, leave empty to get information from all
            nodes
        :arg type_: The type to sample (default: cpu)
        :arg interval: The interval for the second sampling of threads
        :arg snapshots: Number of samples of thread stacktrace (default: 10)
        :arg threads: Specify the number of threads to provide information for
            (default: 3)
        """
        params = {}

        if type_ is not default:
            # avoid python reserved words
            params['type'] = type_
        if interval is not default:
            params['interval'] = interval
        if snapshots is not default:
            params['snapshots'] = snapshots
        if threads is not default:
            params['threads'] = threads

        _, data = yield from self.transport.perform_request(
            'GET', _make_path('_nodes', node_id, 'hot_threads'),
            params=params, decoder=_decode_text
        )
        return data
