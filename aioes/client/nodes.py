import asyncio

from .utils import NamespacedClient
from .utils import _make_path

default = object()


class NodesClient(NamespacedClient):

    @asyncio.coroutine
    def info(self, node_id=None, metric=None, *,
             flat_settings=default, human=default):
        """
        The cluster nodes info API allows to retrieve one or more (or all) of
        the cluster nodes information.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-nodes-info.html>`_

        :arg node_id: A comma-separated list of node IDs or names to limit the
            returned information; use `_local` to return information from the
            node you're connecting to, leave empty to get information from all
            nodes
        :arg metric: A comma-separated list of metrics you wish returned. Leave
            empty to return all. Choices are "settings", "os", "process",
            "jvm", "thread_pool", "network", "transport", "http", "plugin"
        :arg flat_settings: Return settings in flat format (default: false)
        :arg human: Whether to return time and byte values in human-readable
            format., default False
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
