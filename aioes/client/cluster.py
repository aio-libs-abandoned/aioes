import asyncio

from .utils import NamespacedClient
from .utils import _make_path

default = object()


class ClusterClient(NamespacedClient):

    @asyncio.coroutine
    def health(self, index=None, *,
               level=default, local=default, master_timeout=default,
               timeout=default, wait_for_active_shards=default,
               wait_for_nodes=default, wait_for_relocating_shards=default,
               wait_for_status=default):
        """
        Get a very simple status on the health of the cluster.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/
        current/cluster-health.html>`_

        :arg index: Limit the information returned to a specific index
        :arg level: Specify the level of detail for returned information,
             default u'cluster'
        :arg local: Return local information, do not retrieve the state from
             master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to
             master node
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Wait until the specified number of shards
             is active
        :arg wait_for_nodes: Wait until the specified number of nodes is
             available
        :arg wait_for_relocating_shards: Wait until the specified number of
             relocating shards is finished
        :arg wait_for_status: Wait until cluster is in a specific state,
             default None
        """
        params = {}
        if level is not default:
            if not isinstance(level, str):
                raise TypeError("'level' parameter is not a string")
            elif level.lower() in ('cluster', 'indices', 'shards'):
                params['level'] = level.lower()
            else:
                raise ValueError("'level' parameter should be one"
                                 " of 'cluster', 'indices', 'shards'")
        if local is not default:
            params['local'] = bool(local)
        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if timeout is not default:
            params['timeout'] = timeout
        if wait_for_active_shards is not default:
            params['wait_for_active_shards'] = int(wait_for_active_shards)
        if wait_for_nodes is not default:
            params['wait_for_nodes'] = str(wait_for_nodes)
        if wait_for_relocating_shards is not default:
            params['wait_for_relocating_shards'] = \
                int(wait_for_relocating_shards)
        if wait_for_status is not default:
            if not isinstance(wait_for_status, str):
                raise TypeError("'wait_for_status' parameter is not a string")
            elif wait_for_status.lower() in ('green', 'yellow', 'red'):
                params['wait_for_status'] = wait_for_status.lower()
            else:
                raise ValueError("'wait_for_status' parameter should be one"
                                 " of 'green', 'yellow', 'red'")

        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path('_cluster', 'health', index),
            params=params)
        return data

    @asyncio.coroutine
    def pending_tasks(self, *, local=default, master_timeout=default):
        """
        The pending cluster tasks API returns a list of any cluster-level
        changes (e.g. create index, update mapping, allocate or fail shard)
        which have not yet been executed.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-pending.html>`_

        :arg local: Return local information, do not retrieve the state
            from master node (default: false)
        :arg master_timeout: Specify timeout for connection to master
        """
        params = {}

        if local is not default:
            params['local'] = bool(local)
        if master_timeout is not default:
            params['master_timeout'] = master_timeout

        _, data = yield from self.transport.perform_request(
            'GET', '/_cluster/pending_tasks',
            params=params
        )
        return data

    @asyncio.coroutine
    def state(self, metric=None, index=None, *, index_templates=default,
              local=default, master_timeout=default, flat_settings=default):
        """
        Get a comprehensive state information of the whole cluster.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-state.html>`_

        :arg metric: Limit the information returned to the specified metrics.
            Possible values: "_all", "blocks", "index_templates", "metadata",
            "nodes", "routing_table", "master_node", "version"
        :arg index: A comma-separated list of index names; use `_all` or empty
            string to perform the operation on all indices
        :arg index_templates: A comma separated list to return specific index
            templates when returning metadata.
        :arg local: Return local information, do not retrieve the state
            from master node (default: false)
        :arg master_timeout: Specify timeout for connection to master
        :arg flat_settings: Return settings in flat format (default: false)
        """
        params = {}

        if local is not default:
            params['local'] = bool(local)
        if index_templates is not default:
            params['index_templates'] = index_templates
        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if flat_settings is not default:
            params['flat_settings'] = bool(flat_settings)

        if index and not metric:
            metric = '_all'

        _, data = yield from self.transport.perform_request(
            'GET', _make_path('_cluster', 'state', metric, index),
            params=params
        )
        return data

    @asyncio.coroutine
    def stats(self, node_id=None, *, flat_settings=default, human=default):
        """
        The Cluster Stats API allows to retrieve statistics from a cluster wide
        perspective. The API returns basic index metrics and information about
        the current nodes that form the cluster.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-stats.html>`_

        :arg node_id: A comma-separated list of node IDs or names to limit the
            returned information; use `_local` to return information from the
            node you're connecting to, leave empty to get information from
            all nodes
        :arg flat_settings: Return settings in flat format (default: false)
        :arg human: Whether to return time and byte values in
            human-readable format.

        """
        params = {}

        if flat_settings is not default:
            params['flat_settings'] = bool(flat_settings)
        if human is not default:
            params['human'] = bool(human)

        url = '/_cluster/stats'
        if node_id:
            url = _make_path('_cluster/stats/nodes', node_id)
        _, data = yield from self.transport.perform_request(
            'GET', url, params=params
        )
        return data

    @asyncio.coroutine
    def reroute(self, body=None, *, dry_run=default, explain=default,
                filter_metadata=default, master_timeout=default,
                timeout=default):
        """
        Explicitly execute a cluster reroute allocation command including
        specific commands.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-reroute.html>`_

        :arg body: The definition of `commands` to perform
            (`move`, `cancel`, `allocate`)
        :arg dry_run: Simulate the operation only and return
            the resulting state
        :arg explain: Return an explanation of why the commands can or
            cannot be executed
        :arg filter_metadata: Don't return cluster state metadata
            (default: false)
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg timeout: Explicit operation timeout
        """
        params = {}

        if dry_run is not default:
            params['dry_run'] = bool(dry_run)
        if explain is not default:
            params['explain'] = bool(explain)
        if filter_metadata is not default:
            params['filter_metadata'] = bool(filter_metadata)
        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if timeout is not default:
            params['timeout'] = timeout

        _, data = yield from self.transport.perform_request(
            'POST', '/_cluster/reroute', params=params, body=body
        )
        return data

    @asyncio.coroutine
    def get_settings(self, *, flat_settings=default, master_timeout=default,
                     timeout=default):
        """
        Get cluster settings.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-update-settings.html>`_

        :arg flat_settings: Return settings in flat format (default: false)
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg timeout: Explicit operation timeout
        """
        params = {}

        if flat_settings is not default:
            params['flat_settings'] = bool(flat_settings)
        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if timeout is not default:
            params['timeout'] = timeout

        _, data = yield from self.transport.perform_request(
            'GET', '/_cluster/settings', params=params
        )
        return data

    @asyncio.coroutine
    def put_settings(self, body, *, flat_settings=default):
        """
        Update cluster wide specific settings.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-update-settings.html>`_

        :arg body: The settings to be updated. Can be either `transient` or
            `persistent` (survives cluster restart).
        :arg flat_settings: Return settings in flat format (default: false)
        """
        params = {}

        if flat_settings is not default:
            params['flat_settings'] = bool(flat_settings)

        _, data = yield from self.transport.perform_request(
            'PUT', '/_cluster/settings',
            params=params, body=body
        )
        return data
