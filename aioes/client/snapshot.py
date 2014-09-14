import asyncio

from .utils import NamespacedClient
from .utils import _make_path

default = object()


class SnapshotClient(NamespacedClient):

    @asyncio.coroutine
    def status(self, repository=None, snapshot=None, *,
               master_timeout=default):
        """Get snapshot status

        :arg repository: A repository name
        :arg snapshot: A comma-separated list of snapshot names
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        """
        params = {}
        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path('_snapshot', repository, snapshot, '_status'),
            params=params)
        return data
