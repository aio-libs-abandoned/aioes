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
