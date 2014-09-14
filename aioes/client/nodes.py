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
